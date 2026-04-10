"""Phase 4 FastAPI Endpoints"""

from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException

from src.phase2.models import StandardizedPreference
from src.phase3.models import CandidateRetrievalResponse
from .config import Phase4Config
from .models import LLMOrchestrationRequest, LLMRecommendationResponse
from .service import LLMOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/phase4", tags=["phase4"])

# Initialize orchestrator
config = Phase4Config()
orchestrator = LLMOrchestrator(config=config)


@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "phase": "phase4",
        "model": config.groq_model,
        "groq_configured": bool(config.groq_api_key),
    }


@router.post("/recommend", response_model=LLMRecommendationResponse)
def recommend(request: LLMOrchestrationRequest) -> LLMRecommendationResponse:
    """
    Generate LLM-based recommendations.
    
    Takes user preference and candidate restaurants, uses LLM to rank and explain.
    
    Args:
        request: LLMOrchestrationRequest with preference and candidates
        
    Returns:
        LLMRecommendationResponse with ranked recommendations
    """
    try:
        # Validate inputs
        if not request.candidates:
            raise HTTPException(
                status_code=400,
                detail="No candidate restaurants provided",
            )
        
        if len(request.candidates) > 100:
            raise HTTPException(
                status_code=400,
                detail="Too many candidates (max 100)",
            )
        
        # Call orchestrator
        response = orchestrator.recommend(
            preference=request.preference.model_dump(),
            candidates=request.candidates,
            top_k=request.top_k,
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}",
        ) from e


@router.post("/full-flow")
def full_flow(
    preference: StandardizedPreference,
    candidates: list[dict],
    candidate_pool_size: int = 50,
) -> LLMRecommendationResponse:
    """
    End-to-end flow: Takes candidates and returns final recommendations.
    
    This is a convenience endpoint that directly uses Phase 3 output.
    """
    try:
        response = orchestrator.recommend(
            preference=preference.model_dump(),
            candidates=candidates,
            top_k=preference.top_k,
        )
        return response
    except Exception as e:
        logger.error(f"Full flow error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Full flow failed: {str(e)}",
        ) from e
