from __future__ import annotations

import re
import pandas as pd
from datasets import load_dataset

from .config import PipelineConfig
from .normalize import (
    cuisines_to_string,
    dedupe_restaurants,
    normalize_city,
    normalize_cuisines,
    normalize_currency,
    normalize_string,
    parse_cost,
    parse_numeric,
    parse_rating,
)
from .reporting import build_quality_payload, write_reports
from .schema import REQUIRED_COLUMNS, validate_schema


ALIASES = {
    "restaurant_id": ["restaurant id", "id", "res_id", "restaurantid"],
    "name": ["restaurant name", "name", "res_name", "restaurantname"],
    "city": ["city", "location city", "listed_in(city)", "listed_in city", "location"],
    "locality": ["locality", "area", "address locality", "sub locality", "address"],
    "cuisines": ["cuisines", "cuisine", "type of cuisine"],
    "avg_cost_for_two": [
        "average cost for two",
        "cost for two",
        "avg cost",
        "price for two",
        "approx_cost(for two people)",
        "approx cost(for two people)",
        "approx cost",
    ],
    "currency": ["currency", "currency symbol"],
    "rating": ["aggregate rating", "rating", "user rating", "rate"],
    "votes": ["votes", "rating votes"],
}


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower().strip())


def _column_map(columns: list[str]) -> dict[str, str]:
    slug_to_original = {_slug(c): c for c in columns}
    mapped: dict[str, str] = {}
    for target, candidates in ALIASES.items():
        for alias in candidates:
            key = _slug(alias)
            if key in slug_to_original:
                mapped[target] = slug_to_original[key]
                break
    return mapped


def _canonicalize(raw_df: pd.DataFrame) -> pd.DataFrame:
    mapping = _column_map(raw_df.columns.tolist())

    out = pd.DataFrame()
    out["restaurant_id"] = (
        raw_df[mapping["restaurant_id"]]
        if "restaurant_id" in mapping
        else pd.Series(range(1, len(raw_df) + 1))
    )
    out["name"] = (
        raw_df[mapping["name"]].astype(str).str.strip()
        if "name" in mapping
        else "Unknown Restaurant"
    )
    out["city"] = (
        raw_df[mapping["city"]].apply(normalize_city)
        if "city" in mapping
        else "Unknown"
    )
    out["locality"] = (
        raw_df[mapping["locality"]].apply(normalize_string)
        if "locality" in mapping
        else "Unknown"
    )
    out["cuisines"] = (
        raw_df[mapping["cuisines"]].apply(normalize_cuisines)
        if "cuisines" in mapping
        else [["Unknown"]] * len(raw_df)
    )
    out["avg_cost_for_two"] = (
        parse_cost(raw_df[mapping["avg_cost_for_two"]])
        if "avg_cost_for_two" in mapping
        else pd.Series([None] * len(raw_df))
    )
    out["currency"] = (
        raw_df[mapping["currency"]].apply(normalize_currency)
        if "currency" in mapping
        else "INR"
    )
    out["rating"] = (
        parse_rating(raw_df[mapping["rating"]])
        if "rating" in mapping
        else pd.Series([None] * len(raw_df))
    )
    out["votes"] = (
        parse_numeric(raw_df[mapping["votes"]]).fillna(0).astype("Int64")
        if "votes" in mapping
        else pd.Series([0] * len(raw_df), dtype="Int64")
    )

    out["name"] = out["name"].replace("", "Unknown Restaurant")
    out["city"] = out["city"].fillna("Unknown")
    out["locality"] = out["locality"].fillna("Unknown")
    out["cuisines"] = out["cuisines"].apply(cuisines_to_string)
    out["rating"] = out["rating"].fillna(0.0)
    out["rating"] = out["rating"].clip(lower=0, upper=5)
    out["avg_cost_for_two"] = out["avg_cost_for_two"].clip(lower=0)

    out = dedupe_restaurants(out)
    return out


def run_phase1(config: PipelineConfig) -> dict:
    config.ensure_dirs()

    dataset = load_dataset(config.dataset_name, split=config.split)
    raw_df = dataset.to_pandas()
    source_columns = raw_df.columns.tolist()
    raw_df.to_parquet(config.raw_parquet, index=False)

    clean_df = _canonicalize(raw_df)

    for col in REQUIRED_COLUMNS:
        if col not in clean_df.columns:
            clean_df[col] = None

    clean_df = clean_df[REQUIRED_COLUMNS]
    validation = validate_schema(clean_df)

    clean_df.to_parquet(config.processed_parquet, index=False)
    clean_df.to_csv(config.processed_csv, index=False)

    payload = build_quality_payload(raw_df, clean_df, validation, source_columns)
    write_reports(payload, config.quality_report_json, config.quality_report_md)
    return payload

