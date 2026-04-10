"""Phase 4 Output Parser - Parses and validates LLM responses"""

from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class OutputParser:
    """Parses and validates LLM output responses"""

    @staticmethod
    def parse_llm_response(
        raw_response: str,
        candidates: list[dict[str, Any]],
        timeout: int = 5,
    ) -> tuple[bool, dict[str, Any] | None]:
        """
        Parse LLM response and validate structure.
        
        Returns:
            (success: bool, parsed_data: dict or None)
        """
        
        if not raw_response or not raw_response.strip():
            logger.error("Empty LLM response")
            return False, None
        
        # Try direct JSON parsing
        parsed = OutputParser._extract_json(raw_response)
        if not parsed:
            logger.error("Failed to extract JSON from response")
            return False, None
        
        # Validate structure
        is_valid = OutputParser._validate_structure(parsed)
        if not is_valid:
            logger.error(f"Invalid response structure: {parsed}")
            return False, None
        
        # Validate recommendations reference valid candidates
        is_grounded = OutputParser._validate_grounding(
            parsed.get("recommendations", []),
            candidates,
        )
        if not is_grounded:
            logger.warning("Some recommendations reference invalid candidates")
            # Still return the response but log warning
        
        return True, parsed

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any] | None:
        """Extract JSON from text (handles markdown code blocks)"""
        
        text = text.strip()
        
        # Try direct parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try removing markdown code blocks
        if "```json" in text:
            try:
                start = text.index("```json") + 7
                end = text.rindex("```")
                json_str = text[start:end].strip()
                return json.loads(json_str)
            except (ValueError, json.JSONDecodeError):
                pass
        
        if "```" in text:
            try:
                start = text.index("```") + 3
                end = text.rindex("```")
                json_str = text[start:end].strip()
                return json.loads(json_str)
            except (ValueError, json.JSONDecodeError):
                pass
        
        # Try finding JSON object in text
        try:
            start_idx = text.index("{")
            end_idx = text.rindex("}") + 1
            json_str = text[start_idx:end_idx]
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass
        
        logger.error(f"Could not extract JSON from: {text[:100]}...")
        return None

    @staticmethod
    def _validate_structure(data: dict[str, Any]) -> bool:
        """Validate response has required structure"""
        
        required_keys = ["recommendations", "summary"]
        for key in required_keys:
            if key not in data:
                logger.error(f"Missing required key: {key}")
                return False
        
        if not isinstance(data["recommendations"], list):
            logger.error("'recommendations' must be a list")
            return False
        
        if len(data["recommendations"]) == 0:
            logger.error("'recommendations' list is empty")
            return False
        
        # Validate each recommendation
        for i, rec in enumerate(data["recommendations"]):
            required_rec_keys = ["rank", "restaurant_id", "name", "explanation"]
            for key in required_rec_keys:
                if key not in rec:
                    logger.error(f"Recommendation {i} missing '{key}'")
                    return False
            
            # Validate rank is positive integer
            try:
                if not isinstance(rec["rank"], int) or rec["rank"] < 1:
                    logger.error(f"Recommendation {i} has invalid rank: {rec['rank']}")
                    return False
            except (TypeError, ValueError):
                logger.error(f"Recommendation {i} rank must be integer")
                return False
        
        if not isinstance(data["summary"], str):
            logger.error("'summary' must be a string")
            return False
        
        return True

    @staticmethod
    def _validate_grounding(
        recommendations: list[dict[str, Any]],
        candidates: list[dict[str, Any]],
    ) -> bool:
        """Validate that all recommendations reference valid candidates"""
        
        candidate_ids = {str(c.get("restaurant_id", "")) for c in candidates}
        
        for rec in recommendations:
            rec_id = str(rec.get("restaurant_id", ""))
            if rec_id not in candidate_ids:
                logger.warning(
                    f"Recommendation restaurant_id '{rec_id}' not found in candidates"
                )
                return False
        
        return True

    @staticmethod
    def enrich_response(
        parsed_data: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Enrich parsed response with additional candidate data"""
        
        candidates_by_id = {str(c.get("restaurant_id", "")): c for c in candidates}
        
        enriched_recs = []
        for rec in parsed_data.get("recommendations", []):
            rec_id = str(rec.get("restaurant_id", ""))
            candidate = candidates_by_id.get(rec_id, {})
            
            # Add missing fields from candidate
            enriched = {
                **rec,
                "cuisine": rec.get("cuisine", candidate.get("cuisines", "N/A")),
                "rating": rec.get("rating", candidate.get("rating", 0)),
                "estimated_cost": rec.get(
                    "estimated_cost",
                    candidate.get("avg_cost_for_two", 0),
                ),
            }
            enriched_recs.append(enriched)
        
        return {
            **parsed_data,
            "recommendations": enriched_recs,
        }
