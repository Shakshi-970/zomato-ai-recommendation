"""Phase 5 API Endpoints - End-to-End Recommendation"""

from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .service import EndToEndOrchestrator, EndToEndRequest, EndToEndResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/phase5", tags=["phase5"])

# Initialize orchestrator
orchestrator = EndToEndOrchestrator()


class RecommendationRequest(BaseModel):
    """User preference input for recommendations"""
    city: str = Field(..., min_length=1, example="Bengaluru")
    locality: str = Field(..., min_length=1, example="Koramangala")
    budget_tier: str | None = Field(None, example="medium")
    budget: float | None = Field(None, ge=0, example=1500)
    preferred_cuisines: list[str] = Field(default_factory=list, example=["Italian", "Chinese"])
    min_rating: float = Field(default=0.0, ge=0, le=5, example=3.5)
    additional_preferences: list[str] = Field(default_factory=list, example=["family-friendly"])
    top_k: int = Field(default=5, ge=1, le=10, example=5)


class RecommendationResult(BaseModel):
    """Single recommendation in result"""
    rank: int
    name: str
    cuisine: str
    rating: float
    estimated_cost: float
    explanation: str
    source: str


class LocationResponse(BaseModel):
    """Supported cities and localities"""
    cities: list[str]
    localities: list[str]


class RecommendationResponse(BaseModel):
    """Complete end-to-end response"""
    query_id: str
    
    # Phase 2: Preference Validation
    preference_valid: bool
    preference_errors: list[str]
    normalized_preference: dict | None
    
    # Phase 3: Candidate Retrieval
    total_candidates: int
    selected_candidates: int
    
    # Phase 4: LLM Ranking
    recommendations: list[RecommendationResult]
    summary: str
    
    # Metadata
    tokens_used: int
    cost_usd: float


@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "phase": "phase5",
        "service": "end-to-end-orchestration",
    }


@router.get("/locations", response_model=LocationResponse)
def get_locations(city: str | None = None) -> LocationResponse:
    """Return supported cities and locality options."""
    from pathlib import Path
    import pandas as pd

    data_file = Path(__file__).resolve().parents[2] / "data" / "processed" / "restaurants_clean.csv"
    if not data_file.exists():
        return LocationResponse(cities=[], localities=[])

    df = pd.read_csv(data_file, usecols=["city", "locality"])
    df["city"] = df["city"].astype(str).str.strip()
    df["locality"] = df["locality"].astype(str).str.strip()

    cities = sorted(df["city"].dropna().unique())
    selected_city = city if city else (cities[0] if cities else "")
    localities = []
    if selected_city:
        localities = sorted(
            df[df["city"].str.lower() == selected_city.strip().lower()]
            ["locality"].dropna().unique()
        )

    return LocationResponse(cities=cities, localities=localities)


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest) -> RecommendationResponse:
    """
    End-to-end restaurant recommendation.
    
    This endpoint orchestrates the complete workflow:
    1. Validates user preferences (Phase 2)
    2. Retrieves candidate restaurants (Phase 3)
    3. Ranks with LLM and generates explanations (Phase 4)
    4. Returns formatted recommendations
    
    Args:
        request: User preference input
        
    Returns:
        RecommendationResponse with ranked recommendations and metadata
    """
    try:
        # Convert to internal request
        e2e_request = EndToEndRequest(
            city=request.city,
            locality=request.locality,
            budget_tier=request.budget_tier,
            budget=request.budget,
            preferred_cuisines=request.preferred_cuisines,
            min_rating=request.min_rating,
            additional_preferences=request.additional_preferences,
            top_k=request.top_k,
        )
        
        # Get response
        response = orchestrator.recommend(e2e_request)
        
        # Convert to API response
        return RecommendationResponse(
            query_id=response.query_id,
            preference_valid=response.preference_valid,
            preference_errors=response.preference_errors,
            normalized_preference=response.normalized_preference,
            total_candidates=response.total_candidates,
            selected_candidates=response.selected_candidates,
            recommendations=[
                RecommendationResult(**rec) for rec in response.recommendations
            ],
            summary=response.summary,
            tokens_used=response.tokens_used,
            cost_usd=response.cost_usd,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}",
        ) from e
