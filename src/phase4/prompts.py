"""Prompt Templates for Phase 4 LLM Orchestration"""

from __future__ import annotations

import json
from typing import Any


class PromptEngine:
    """Manages prompt templates for LLM-based recommendations"""

    SYSTEM_PROMPT = """You are an expert restaurant recommendation AI. Your role is to:
1. Analyze user preferences (location, budget, cuisine, rating requirements)
2. Evaluate candidate restaurants provided by the retrieval system
3. Rank restaurants based on how well they match user preferences
4. Provide clear, concise explanations for each recommendation

Guidelines:
- Prioritize restaurants that match user's preferred cuisines
- Respect budget constraints strictly
- Consider ratings and customer votes as quality indicators
- Explain trade-offs when recommending restaurants outside primary preferences
- Return ONLY valid JSON, no markdown, no additional text"""

    @staticmethod
    def build_user_prompt(
        preference: dict[str, Any],
        candidates: list[dict[str, Any]],
        top_k: int = 5,
    ) -> str:
        """Build user prompt with preference and candidate data"""
        
        # Format preference
        pref_str = PromptEngine._format_preference(preference)
        
        # Format candidates
        candidates_str = PromptEngine._format_candidates(candidates)
        
        prompt = f"""Given the following user preference and candidate restaurants, rank the top {top_k} restaurants that best match the user's needs.

USER PREFERENCE:
{pref_str}

CANDIDATE RESTAURANTS (already pre-filtered by relevance):
{candidates_str}

Return ONLY valid JSON in this exact format with no markdown or extra text:
{{
  "recommendations": [
    {{
      "rank": 1,
      "restaurant_id": "...",
      "name": "...",
      "cuisine": "...",
      "rating": ...,
      "estimated_cost": ...,
      "explanation": "Clear explanation of why this matches the user's preferences"
    }}
  ],
  "summary": "Brief summary of the top picks and why they are recommended"
}}"""
        
        return prompt

    @staticmethod
    def _format_preference(pref: dict[str, Any]) -> str:
        """Format preference as readable text"""
        min_rating = pref.get('min_rating', 0.0)
        lines = [
            f"- Location: {pref.get('location', 'N/A')}",
            f"- Budget Tier: {pref.get('budget_tier', 'N/A')} (estimated range)",
            f"- Preferred Cuisines: {', '.join(pref.get('preferred_cuisines', ['Any']))}",
            f"- Minimum Rating: {min_rating}/5.0 (STRICT: only include restaurants with rating >= {min_rating}; prefer higher-rated ones)",
        ]
        if pref.get('additional_preferences'):
            lines.append(f"- Additional Preferences: {', '.join(pref.get('additional_preferences', []))}")
        lines.append(f"- Top K Results Requested: {pref.get('top_k', 5)}")
        return "\n".join(lines)

    @staticmethod
    def _format_candidates(candidates: list[dict[str, Any]]) -> str:
        """Format candidates as readable table"""
        lines = []
        for i, c in enumerate(candidates[:15], 1):  # Limit to 15 candidates
            cuisine = c.get('cuisines', 'N/A')
            rating = c.get('rating', 0)
            cost = c.get('avg_cost_for_two', 0)
            votes = c.get('votes', 0)
            score = c.get('final_score', c.get('pre_rank_score', 0))
            city = c.get('city', '')
            locality = c.get('locality', '')
            
            line = (
                f"{i}. {c.get('name', 'N/A')} (ID: {c.get('restaurant_id', 'N/A')}) "
                f"| Cuisines: {cuisine} | Rating: {rating} | Cost: ₹{cost} "
                f"| Votes: {votes} | City: {city} | Locality: {locality} | Pre-score: {score:.3f}"
            )
            lines.append(line)
        
        return "\n".join(lines)

    @staticmethod
    def get_fallback_system_prompt() -> str:
        """System prompt for fallback heuristic ranking"""
        return """You are a restaurant recommendation expert using heuristic-based ranking (not LLM).
Provide clear recommendations based on pre-computed relevance scores without deep reasoning.
Return valid JSON only."""
