from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PreferenceValidationRequest(BaseModel):
    city: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    budget_tier: str | None = None
    budget_for_two: float | None = Field(default=None, ge=0)
    preferred_cuisines: list[str] = Field(default_factory=list)
    min_rating: float = Field(default=0.0, ge=0, le=5)
    additional_preferences: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=10)


class StandardizedPreference(BaseModel):
    city: str
    location: str
    budget_tier: Literal["low", "medium", "high"]
    budget_amount: float | None = None
    preferred_cuisines: list[str]
    min_rating: float
    additional_preferences: list[str]
    top_k: int


class PreferenceValidationResponse(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)
    normalized: StandardizedPreference | None = None

