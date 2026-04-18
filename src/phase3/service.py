from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import pandas as pd

from src.phase2.models import StandardizedPreference

from .cache import TTLCache
from .config import Phase3Config
from .models import CandidateRetrievalResponse, CandidateRestaurant, GroqLLMInput


@dataclass
class CandidateRetrievalService:
    config: Phase3Config

    def __post_init__(self) -> None:
        self.scoring = self.config.load_scoring()
        self.weights = self.scoring["weights"]
        self.budget_ranges = self.scoring["budget_ranges"]
        self.default_candidate_pool_size = int(self.scoring["candidate_pool_size"])
        self.cache = TTLCache(self.config.candidate_cache_ttl_seconds)
        self.df = pd.read_csv(self.config.data_file)
        self.df["city"] = self.df["city"].astype(str).str.strip()
        self.df["locality"] = self.df["locality"].astype(str).str.strip()
        self.df["city_norm"] = self.df["city"].str.lower()
        self.df["locality_norm"] = self.df["locality"].str.lower()
        self.df["rating"] = pd.to_numeric(self.df["rating"], errors="coerce").fillna(0.0)
        self.df["avg_cost_for_two"] = pd.to_numeric(
            self.df["avg_cost_for_two"], errors="coerce"
        ).fillna(0.0)
        self.df["votes"] = pd.to_numeric(self.df["votes"], errors="coerce").fillna(0).astype(int)

    def _cache_key(self, pref: StandardizedPreference, pool_size: int) -> str:
        raw = json.dumps({"pref": pref.model_dump(), "pool_size": pool_size}, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _budget_window(self, tier: str) -> tuple[float, float]:
        low, high = self.budget_ranges[tier]
        return float(low), float(high)

    @staticmethod
    def _safe_ratio(numerator: float, denominator: float) -> float:
        if denominator <= 0:
            return 0.0
        return max(0.0, min(1.0, numerator / denominator))

    def _score_row(self, row: pd.Series, pref: StandardizedPreference) -> tuple[float, dict, list[str]]:
        cuisines = [c.strip().lower() for c in str(row["cuisines"]).split(",") if c.strip()]
        requested = [c.strip().lower() for c in pref.preferred_cuisines]
        pref_tags = [p.strip().lower() for p in pref.additional_preferences]
        text_blob = f"{row.get('name', '')} {row.get('city', '')} {row.get('locality', '')} {row.get('cuisines', '')}".lower()

        cuisine_hits = len(set(cuisines).intersection(set(requested))) if requested else 0
        cuisine_match = self._safe_ratio(cuisine_hits, max(1, len(requested))) if requested else 1.0
        rating_score = self._safe_ratio(float(row["rating"]), 5.0)

        cost = float(row["avg_cost_for_two"])
        if pref.budget_amount is not None and pref.budget_amount > 0:
            b = float(pref.budget_amount)
            budget_fit = 1.0 if (b >= 1000 and cost >= b) or (b < 1000 and b <= cost < b + 100.0) else 0.0
        else:
            min_budget, max_budget = self._budget_window(pref.budget_tier)
            budget_fit = 1.0 if min_budget <= cost <= max_budget else 0.0

        matched_tags = [p for p in pref_tags if p in text_blob]
        preference_tag_match = self._safe_ratio(len(matched_tags), max(1, len(pref_tags))) if pref_tags else 1.0

        final = (
            self.weights["cuisine_match"] * cuisine_match
            + self.weights["rating_score"] * rating_score
            + self.weights["budget_fit"] * budget_fit
            + self.weights["preference_tag_match"] * preference_tag_match
        )
        breakdown = {
            "cuisine_match": round(cuisine_match, 4),
            "rating_score": round(rating_score, 4),
            "budget_fit": round(budget_fit, 4),
            "preference_tag_match": round(preference_tag_match, 4),
        }
        return round(final, 6), breakdown, matched_tags

    @staticmethod
    def _dedupe_candidates(rows: list[dict]) -> list[dict]:
        unique: dict[str, dict] = {}
        for row in rows:
            restaurant_id = str(row.get("restaurant_id", "")).strip()
            name_key = str(row.get("name", "")).strip().lower()
            key = restaurant_id or name_key
            if not key:
                continue

            existing = unique.get(key)
            if existing is None:
                unique[key] = row
                continue

            replace = False
            if row["final_score"] > existing["final_score"]:
                replace = True
            elif row["final_score"] == existing["final_score"] and row["rating"] > existing["rating"]:
                replace = True
            elif row["final_score"] == existing["final_score"] and row["rating"] == existing["rating"] and row["votes"] > existing["votes"]:
                replace = True

            if replace:
                unique[key] = row

        return list(unique.values())

    def retrieve(self, pref: StandardizedPreference, candidate_pool_size: int | None = None) -> CandidateRetrievalResponse:
        pool_size = candidate_pool_size or self.default_candidate_pool_size
        key = self._cache_key(pref, pool_size)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        min_budget, max_budget = self._budget_window(pref.budget_tier)
        city_match = self.df["city_norm"] == pref.city.strip().lower()
        if pref.location:
            locality_match = self.df["locality_norm"] == pref.location.strip().lower()
            location_mask = city_match & locality_match
        else:
            location_mask = city_match

        # Rating filter: minimum rating — show all restaurants rated >= min_rating
        if pref.min_rating > 0:
            rating_mask = self.df["rating"] >= float(int(pref.min_rating))
        else:
            rating_mask = self.df["rating"] >= 0.0

        # Budget filter: [budget, budget+100) for <1000; >=1000 for budget>=1000
        if pref.budget_amount is not None and pref.budget_amount > 0:
            b = float(pref.budget_amount)
            if b >= 1000:
                budget_mask = self.df["avg_cost_for_two"] >= b
            else:
                budget_mask = (self.df["avg_cost_for_two"] >= b) & (self.df["avg_cost_for_two"] < b + 100.0)
        else:
            budget_mask = self.df["avg_cost_for_two"] >= 0.0

        filtered = self.df[
            location_mask
            & rating_mask
            & budget_mask
        ].copy()

        if filtered.empty:
            response = CandidateRetrievalResponse(
                llm_provider=self.config.llm_provider,
                groq_api_key_configured=bool(self.config.groq_api_key),
                total_after_filtering=0,
                selected_count=0,
                candidates=[],
            )
            self.cache.set(key, response)
            return response

        scored_rows: list[dict] = []
        for _, row in filtered.iterrows():
            final_score, breakdown, matched_tags = self._score_row(row, pref)
            scored_rows.append(
                {
                    "restaurant_id": str(row["restaurant_id"]),
                    "name": str(row["name"]),
                    "city": str(row["city"]),
                    "locality": str(row["locality"]),
                    "cuisines": str(row["cuisines"]),
                    "avg_cost_for_two": float(row["avg_cost_for_two"]),
                    "rating": float(row["rating"]),
                    "votes": int(row["votes"]),
                    "final_score": float(final_score),
                    "score_breakdown": breakdown,
                    "matched_preferences": matched_tags,
                }
            )

        ranked = sorted(scored_rows, key=lambda x: (x["final_score"], x["rating"], x["votes"]), reverse=True)
        unique_ranked = self._dedupe_candidates(ranked)
        top_rows = unique_ranked[:pool_size]
        candidates = [CandidateRestaurant(**item) for item in top_rows]

        response = CandidateRetrievalResponse(
            llm_provider=self.config.llm_provider,
            groq_api_key_configured=bool(self.config.groq_api_key),
            total_after_filtering=len(scored_rows),
            selected_count=len(candidates),
            candidates=candidates,
        )
        self.cache.set(key, response)
        return response

    def build_groq_input(self, pref: StandardizedPreference, candidate_pool_size: int | None = None) -> GroqLLMInput:
        response = self.retrieve(pref, candidate_pool_size)
        table = [
            {
                "restaurant_id": c.restaurant_id,
                "name": c.name,
                "city": c.city,
                "locality": c.locality,
                "cuisines": c.cuisines,
                "avg_cost_for_two": c.avg_cost_for_two,
                "rating": c.rating,
                "votes": c.votes,
                "pre_rank_score": c.final_score,
            }
            for c in response.candidates
        ]
        return GroqLLMInput(
            llm_provider=self.config.llm_provider,
            preference=pref,
            candidate_table=table,
        )

