from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from .schema import ValidationResult


def build_quality_payload(
    raw_df: pd.DataFrame,
    clean_df: pd.DataFrame,
    validation: ValidationResult,
    source_columns: list[str],
) -> dict:
    return {
        "source_columns": source_columns,
        "raw_record_count": int(len(raw_df)),
        "clean_record_count": int(len(clean_df)),
        "duplicates_removed": int(len(raw_df) - len(clean_df)),
        "schema_validation": asdict(validation) | {"pass_rate": validation.pass_rate},
        "distribution": {
            "top_cities": clean_df["city"].value_counts().head(10).to_dict()
            if "city" in clean_df.columns
            else {},
            "rating_summary": clean_df["rating"].describe().to_dict()
            if "rating" in clean_df.columns
            else {},
        },
    }


def write_reports(payload: dict, json_path: Path, md_path: Path) -> None:
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    schema = payload.get("schema_validation", {})
    md = [
        "# Phase 1 Data Quality Report",
        "",
        f"- Raw records: **{payload.get('raw_record_count', 0)}**",
        f"- Clean records: **{payload.get('clean_record_count', 0)}**",
        f"- Duplicates removed: **{payload.get('duplicates_removed', 0)}**",
        f"- Schema pass rate: **{schema.get('pass_rate', 0)}%**",
        "",
        "## Missing Columns",
    ]
    missing_cols = schema.get("missing_columns", [])
    if missing_cols:
        md.extend([f"- {c}" for c in missing_cols])
    else:
        md.append("- None")

    md.extend(["", "## Top Cities"])
    for city, count in payload.get("distribution", {}).get("top_cities", {}).items():
        md.append(f"- {city}: {count}")

    md.extend(["", "## Rating Summary"])
    rating_summary = payload.get("distribution", {}).get("rating_summary", {})
    if rating_summary:
        for key, value in rating_summary.items():
            md.append(f"- {key}: {round(float(value), 4)}")
    else:
        md.append("- Not available")

    md_path.write_text("\n".join(md), encoding="utf-8")

