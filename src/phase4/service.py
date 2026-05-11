"""Phase 4 LLM Orchestration Service"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from groq import Groq

from .config import Phase4Config
from .models import LLMRecommendationResponse, Recommendation
from .parser import OutputParser
from .prompts import PromptEngine

logger = logging.getLogger(__name__)


class LLMOrchestrator:
    """Orchestrates LLM-based restaurant recommendation"""

    def __init__(self, config: Phase4Config | None = None):
        self.config = config or Phase4Config()
        self.client = Groq(api_key=self.config.groq_api_key)
        self.prompt_engine = PromptEngine()
        self.parser = OutputParser()

    def recommend(
        self,
        preference: dict[str, Any],
        candidates: list[dict[str, Any]],
        top_k: int = 5,
    ) -> LLMRecommendationResponse:
        """
        Generate LLM-based recommendations.
        
        Args:
            preference: StandardizedPreference as dict
            candidates: List of candidate restaurants from Phase 3
            top_k: Number of top recommendations to return
            
        Returns:
            LLMRecommendationResponse with ranked recommendations
        """
        
        query_id = f"q_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        logger.info(f"[{query_id}] Starting LLM recommendation orchestration")
        
        # Build prompt
        user_prompt = self.prompt_engine.build_user_prompt(
            preference, candidates, top_k=top_k
        )
        
        # Call LLM with retry logic
        llm_response, tokens_used = self._call_llm_with_retry(user_prompt)
        
        # Parse response
        parse_success, parsed_data = self.parser.parse_llm_response(
            llm_response, candidates
        )
        
        # Fallback if parsing failed
        fallback_used = False
        if not parse_success:
            logger.warning(f"[{query_id}] LLM parsing failed, using fallback")
            parsed_data = self._generate_fallback_response(
                preference, candidates, top_k
            )
            fallback_used = True
        
        # Enrich response
        enriched_data = self.parser.enrich_response(parsed_data, candidates)
        
        # Build recommendations
        recommendations = [
            Recommendation(
                rank=int(rec.get("rank", i + 1)),
                restaurant_id=str(rec.get("restaurant_id", "")),
                name=str(rec.get("name", "")),
                cuisine=str(rec.get("cuisine", "")),
                rating=float(rec.get("rating", 0)),
                estimated_cost=float(rec.get("estimated_cost", 0)),
                explanation=str(rec.get("explanation", "")),
                source="llm" if not fallback_used else "fallback",
            )
            for i, rec in enumerate(enriched_data.get("recommendations", [])[:top_k])
        ]
        
        # Calculate cost
        cost_usd = (tokens_used / 1000) * self.config.token_cost_per_1k
        
        response = LLMRecommendationResponse(
            query_id=query_id,
            llm_model=self.config.groq_model,
            parse_success=parse_success,
            fallback_used=fallback_used,
            recommendations=recommendations,
            summary=enriched_data.get("summary", "Recommendations generated successfully"),
            tokens_used=tokens_used,
            cost_usd=cost_usd,
        )
        
        logger.info(
            f"[{query_id}] Recommendation complete: "
            f"{len(recommendations)} recommendations, "
            f"{tokens_used} tokens, fallback={fallback_used}"
        )
        
        return response

    def _call_llm_with_retry(self, user_prompt: str) -> tuple[str, int]:
        """Call Groq API with retry logic"""
        
        attempt = 0
        last_error = None
        
        while attempt < self.config.max_retries:
            try:
                start = time.time()
                response = self.client.chat.completions.create(
                    model=self.config.groq_model,
                    messages=[
                        {
                            "role": "system",
                            "content": self.prompt_engine.SYSTEM_PROMPT,
                        },
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    timeout=self.config.timeout_seconds,
                )
                elapsed = time.time() - start
                
                tokens = response.usage.total_tokens if hasattr(response, "usage") else 0
                logger.info(
                    f"LLM call successful in {elapsed:.2f}s with {tokens} tokens"
                )
                
                content = response.choices[0].message.content
                return content, tokens
                
            except Exception as e:
                last_error = e
                attempt += 1
                logger.warning(
                    f"LLM call failed (attempt {attempt}/{self.config.max_retries}): {e}"
                )
                
                if attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay_seconds)
        
        logger.error(f"All LLM retry attempts failed: {last_error}")
        raise RuntimeError(f"LLM call failed after {self.config.max_retries} retries") from last_error

    def _generate_fallback_response(
        self,
        preference: dict[str, Any],
        candidates: list[dict[str, Any]],
        top_k: int,
    ) -> dict[str, Any]:
        """Generate fallback response using heuristic ranking"""
        
        # Sort by pre-computed score
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.get("final_score", x.get("pre_rank_score", 0)),
            reverse=True,
        )
        
        recommendations = []
        for rank, candidate in enumerate(sorted_candidates[:top_k], 1):
            rec = {
                "rank": rank,
                "restaurant_id": candidate.get("restaurant_id", ""),
                "name": candidate.get("name", ""),
                "cuisine": candidate.get("cuisines", ""),
                "rating": candidate.get("rating", 0),
                "estimated_cost": candidate.get("avg_cost_for_two", 0),
                "explanation": (
                    f"Recommended based on heuristic scoring: "
                    f"Good match for {preference.get('budget_tier', 'your')} budget, "
                    f"rating {candidate.get('rating', 0)}/5.0 with strong relevance score."
                ),
            }
            recommendations.append(rec)
        
        return {
            "recommendations": recommendations,
            "summary": (
                f"Fallback recommendations (heuristic ranking): "
                f"Top {len(recommendations)} matches for your preferences."
            ),
        }
