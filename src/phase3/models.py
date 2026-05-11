from __future__ import annotations

from pydantic import BaseModel, Field

from src.phase2.models import StandardizedPreference


class CandidateRestaurant(BaseModel):
    restaurant_id: str
    name: str
    city: str
    locality: str
    cuisines: str
    avg_cost_for_two: float | None = None
    rating: float
    votes: int
    final_score: float
    score_breakdown: dict[str, float]
    matched_preferences: list[str] = Field(default_factory=list)


class CandidateRetrievalRequest(BaseModel):
    preference: StandardizedPreference
    candidate_pool_size: int = Field(default=50, ge=1, le=100)


class CandidateRetrievalResponse(BaseModel):
    llm_provider: str
    groq_api_key_configured: bool
    total_after_filtering: int
    selected_count: int
    candidates: list[CandidateRestaurant]


class GroqLLMInput(BaseModel):
    llm_provider: str = "groq"
    preference: StandardizedPreference
    candidate_table: list[dict]

