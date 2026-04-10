"""Phase 4 Data Models"""

from __future__ import annotations

from pydantic import BaseModel, Field
from src.phase2.models import StandardizedPreference


class Recommendation(BaseModel):
    """Individual restaurant recommendation"""
    
    rank: int
    restaurant_id: str
    name: str
    cuisine: str
    rating: float
    estimated_cost: float
    explanation: str
    source: str = "llm"  # "llm" or "fallback"


class LLMRecommendationResponse(BaseModel):
    """Complete LLM recommendation response"""
    
    query_id: str
    llm_model: str
    parse_success: bool
    fallback_used: bool
    recommendations: list[Recommendation]
    summary: str
    tokens_used: int = 0
    cost_usd: float = 0.0


class LLMOrchestrationRequest(BaseModel):
    """Request for LLM orchestration"""
    
    preference: StandardizedPreference
    candidates: list[dict] = Field(..., description="List of candidate restaurants from Phase 3")
    top_k: int = Field(default=5, ge=1, le=10)
    llm_model: str = Field(default="groq/llama-3.1-8b-instant")
