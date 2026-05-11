from __future__ import annotations

from pathlib import Path

import pandas as pd

from .dictionaries import budget_aliases, city_aliases, preference_aliases


def _norm_text(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


def canonical_cuisine(value: str) -> str:
    text = _norm_text(value)
    return text.title() if text else ""


def canonical_preference(value: str) -> str:
    text = _norm_text(value)
    if not text:
        return ""
    return preference_aliases().get(text, text)


def infer_budget_tier(budget_tier: str | None, budget_for_two: float | None) -> str:
    if budget_tier:
        mapped = budget_aliases().get(_norm_text(budget_tier))
        if mapped:
            return mapped
    if budget_for_two is None:
        return "medium"
    if budget_for_two < 800:
        return "low"
    if budget_for_two <= 1800:
        return "medium"
    return "high"


def load_known_cities(data_file: Path) -> set[str]:
    if not data_file.exists():
        return set()
    df = pd.read_csv(data_file, usecols=["city", "locality"])
    city_values = set(df["city"].dropna().astype(str).str.strip())
    locality_values = set(df["locality"].dropna().astype(str).str.strip())

    # Include both cities and localities as known locations
    return city_values | locality_values


def normalize_location(location: str, known_cities: set[str]) -> str | None:
    text = _norm_text(location)
    if not text:
        return None

    aliased = city_aliases().get(text)
    candidate = aliased if aliased is not None else text.title()

    if not known_cities:
        return candidate

    lower_map = {c.lower(): c for c in known_cities}

    if candidate in known_cities:
        return candidate

    if candidate.lower() in lower_map:
        return lower_map[candidate.lower()]

    if text in lower_map:
        return lower_map[text]

    return None

