from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


CITY_ALIASES = {
    "bengaluru": "Bangalore",
    "bangalore urban": "Bangalore",
    "new delhi": "Delhi",
    "ncr": "Delhi",
    "mumbai suburban": "Mumbai",
}


def to_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    if not value:
        return "Unknown"
    return value.title()


def normalize_city(value: str) -> str:
    raw = re.sub(r"\s+", " ", str(value or "").strip().lower())
    if not raw:
        return "Unknown"
    if raw in CITY_ALIASES:
        return CITY_ALIASES[raw]
    return to_title(raw)


def normalize_cuisines(value: str) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return ["Unknown"]
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if not parts:
        return ["Unknown"]
    return [to_title(p.lower()) for p in parts]


def normalize_currency(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return "INR"
    return text.upper()


def normalize_string(value: str, fallback: str = "Unknown") -> str:
    text = str(value or "").strip()
    return to_title(text.lower()) if text else fallback


def parse_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def parse_rating(series: pd.Series) -> pd.Series:
    # Handles values such as "4.1/5", "NEW", "-", and plain numeric strings.
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace("/5", "", regex=False)
        .str.replace("NEW", "", regex=False)
        .str.replace("-", "", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def parse_cost(series: pd.Series) -> pd.Series:
    # Handles values such as "1,200" and numeric-like strings.
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def dedupe_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    subset = ["name", "city", "locality", "cuisines"]
    for col in subset:
        if col not in df.columns:
            df[col] = "Unknown"
    return df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)


def cuisines_to_string(cuisine_list: Iterable[str]) -> str:
    if isinstance(cuisine_list, list):
        return ", ".join(cuisine_list)
    return str(cuisine_list)

