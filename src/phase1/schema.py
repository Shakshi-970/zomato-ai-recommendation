from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = [
    "restaurant_id",
    "name",
    "city",
    "locality",
    "cuisines",
    "avg_cost_for_two",
    "currency",
    "rating",
    "votes",
]


@dataclass
class ValidationResult:
    total_rows: int
    valid_rows: int
    invalid_rows: int
    missing_columns: list[str]
    nulls_by_column: dict[str, int]

    @property
    def pass_rate(self) -> float:
        if self.total_rows == 0:
            return 0.0
        return round((self.valid_rows / self.total_rows) * 100, 2)


def validate_schema(df: pd.DataFrame) -> ValidationResult:
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    nulls = {col: int(df[col].isna().sum()) for col in df.columns}

    required_for_validity = ["restaurant_id", "name", "city", "cuisines", "rating"]
    valid_mask = pd.Series([True] * len(df))
    for col in required_for_validity:
        if col in df.columns:
            valid_mask &= ~df[col].isna()
            valid_mask &= df[col].astype(str).str.strip() != ""
        else:
            valid_mask &= False

    total = len(df)
    valid = int(valid_mask.sum())
    invalid = total - valid
    return ValidationResult(
        total_rows=total,
        valid_rows=valid,
        invalid_rows=invalid,
        missing_columns=missing_cols,
        nulls_by_column=nulls,
    )

