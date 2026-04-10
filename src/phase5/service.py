"""Phase 5 Orchestration Service - Coordinates Phases 2-4"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from src.phase2.models import PreferenceValidationRequest, PreferenceValidationResponse
from src.phase2.service import PreferenceService
from src.phase3.service import CandidateRetrievalService
from src.phase3.config import Phase3Config
from src.phase4.service import LLMOrchestrator
from src.phase4.config import Phase4Config

logger = logging.getLogger(__name__)


@dataclass
class EndToEndRequest:
    """Request for end-to-end recommendation"""
    city: str
    locality: str
    budget_tier: str | None = None
    budget: float | None = None
    preferred_cuisines: list[str] | None = None
    min_rating: float = 0.0
    additional_preferences: list[str] | None = None
    top_k: int = 5


@dataclass
class EndToEndResponse:
    """Complete end-to-end response with all phases"""
    query_id: str
    
    # Phase 2 results
    preference_valid: bool
    preference_errors: list[str]
    normalized_preference: dict | None
    
    # Phase 3 results
    total_candidates: int
    selected_candidates: int
    
    # Phase 4 results
    recommendations: list[dict]
    summary: str
    
    # Metadata
    tokens_used: int
    cost_usd: float


class EndToEndOrchestrator:
    """Orchestrates complete recommendation flow (Phases 2-4)"""
    
    def __init__(self):
        self.pref_service = PreferenceService(
            known_cities_file=Path("data/processed/restaurants_clean.csv")
        )
        self.candidate_service = CandidateRetrievalService(
            config=Phase3Config()
        )
        self.llm_service = LLMOrchestrator(
            config=Phase4Config()
        )
    
    def recommend(self, request: EndToEndRequest) -> EndToEndResponse:
        """
        End-to-end recommendation workflow.
        
        Flow:
          1. Validate & normalize preference (Phase 2)
          2. Retrieve candidates (Phase 3)
          3. Generate LLM ranking (Phase 4)
          4. Format response
        """
        
        import uuid
        import time
        
        query_id = f"e2e_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        logger.info(f"[{query_id}] Starting end-to-end recommendation workflow")
        
        # ──────────────────────────────────────────────────────────────────
        # PHASE 2: Validate Preference
        # ──────────────────────────────────────────────────────────────────
        
        pref_request = PreferenceValidationRequest(
            city=request.city,
            location=request.locality,
            budget_tier=request.budget_tier,
            budget_for_two=request.budget,
            preferred_cuisines=request.preferred_cuisines or [],
            min_rating=request.min_rating,
            additional_preferences=request.additional_preferences or [],
            top_k=request.top_k,
        )
        
        pref_response = self.pref_service.validate_and_normalize(pref_request)
        
        if not pref_response.valid:
            logger.warning(f"[{query_id}] Preference validation failed: {pref_response.errors}")
            return EndToEndResponse(
                query_id=query_id,
                preference_valid=False,
                preference_errors=pref_response.errors,
                normalized_preference=None,
                total_candidates=0,
                selected_candidates=0,
                recommendations=[],
                summary="Preference validation failed",
                tokens_used=0,
                cost_usd=0.0,
            )
        
        logger.info(f"[{query_id}] Phase 2 (Preference Validation) ✅")
        
        # ──────────────────────────────────────────────────────────────────
        # PHASE 3: Retrieve Candidates
        # ──────────────────────────────────────────────────────────────────
        
        candidates_response = self.candidate_service.retrieve(
            pref_response.normalized,
            candidate_pool_size=50,
        )
        
        candidates = [c.model_dump() for c in candidates_response.candidates]
        
        if not candidates:
            logger.warning(f"[{query_id}] No candidates found")
            return EndToEndResponse(
                query_id=query_id,
                preference_valid=True,
                preference_errors=[],
                normalized_preference=pref_response.normalized.model_dump(),
                total_candidates=candidates_response.total_after_filtering,
                selected_candidates=0,
                recommendations=[],
                summary="No restaurants found matching your criteria",
                tokens_used=0,
                cost_usd=0.0,
            )
        
        logger.info(f"[{query_id}] Phase 3 (Candidate Retrieval) ✅ - {len(candidates)} candidates")
        
        # ──────────────────────────────────────────────────────────────────
        # PHASE 4: LLM Ranking
        # ──────────────────────────────────────────────────────────────────
        
        llm_response = self.llm_service.recommend(
            preference=pref_response.normalized.model_dump(),
            candidates=candidates,
            top_k=request.top_k,
        )
        
        logger.info(f"[{query_id}] Phase 4 (LLM Ranking) ✅ - {len(llm_response.recommendations)} recommendations")
        
        # ──────────────────────────────────────────────────────────────────
        # Format Final Response
        # ──────────────────────────────────────────────────────────────────
        
        recommendations = [
            {
                "rank": rec.rank,
                "name": rec.name,
                "cuisine": rec.cuisine,
                "rating": rec.rating,
                "estimated_cost": rec.estimated_cost,
                "explanation": rec.explanation,
                "source": rec.source,
            }
            for rec in llm_response.recommendations
        ]
        
        response = EndToEndResponse(
            query_id=query_id,
            preference_valid=True,
            preference_errors=[],
            normalized_preference=pref_response.normalized.model_dump(),
            total_candidates=candidates_response.total_after_filtering,
            selected_candidates=len(candidates),
            recommendations=recommendations,
            summary=llm_response.summary,
            tokens_used=llm_response.tokens_used,
            cost_usd=llm_response.cost_usd,
        )
        
        logger.info(f"[{query_id}] End-to-end workflow complete ✅")
        return response
