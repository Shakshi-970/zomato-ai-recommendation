from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .models import (
    PreferenceValidationRequest,
    PreferenceValidationResponse,
    StandardizedPreference,
)
from .normalization import (
    canonical_cuisine,
    canonical_preference,
    infer_budget_tier,
    normalize_location,
)


@dataclass
class PreferenceService:
    known_cities_file: Path

    def __post_init__(self) -> None:
        df = pd.read_csv(self.known_cities_file, usecols=["city", "locality"])
        cities = set(df["city"].dropna().astype(str).str.strip())
        localities = set(df["locality"].dropna().astype(str).str.strip())
        self.known_cities = cities | localities
        self.known_city_names = cities

    def validate_and_normalize(
        self, request: PreferenceValidationRequest
    ) -> PreferenceValidationResponse:
        errors: list[str] = []

        city = normalize_location(request.city, self.known_cities)
        if not city or city not in self.known_city_names:
            supported_cities = ", ".join(sorted(self.known_city_names)) or "<none>"
            errors.append(f"city is required and must be one of: {supported_cities}")

        location = normalize_location(request.location, self.known_cities)
        if not location:
            errors.append("locality is required and must be provided")

        budget_tier = infer_budget_tier(request.budget_tier, request.budget_for_two)
        if budget_tier not in {"low", "medium", "high"}:
            errors.append("budget_tier must resolve to low, medium, or high")

        if not (0 <= request.min_rating <= 5):
            errors.append("min_rating must be between 0 and 5")

        if not (1 <= request.top_k <= 10):
            errors.append("top_k must be between 1 and 10")

        cuisines = [canonical_cuisine(c) for c in request.preferred_cuisines if c.strip()]
        preferences = [
            canonical_preference(p) for p in request.additional_preferences if p.strip()
        ]
        preferences = [p for p in preferences if p]

        if errors:
            return PreferenceValidationResponse(valid=False, errors=errors, normalized=None)

        normalized = StandardizedPreference(
            city=city,
            location=location,  # type: ignore[arg-type]
            budget_tier=budget_tier,  # type: ignore[arg-type]
            budget_amount=float(request.budget_for_two) if request.budget_for_two is not None else None,
            preferred_cuisines=sorted(set(cuisines)),
            min_rating=float(request.min_rating),
            additional_preferences=sorted(set(preferences)),
            top_k=request.top_k,
        )
        return PreferenceValidationResponse(valid=True, errors=[], normalized=normalized)

