"""Phase 4 Configuration"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Phase4Config:
    """Configuration for Phase 4 LLM Orchestration Service"""

    # Groq API Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = "llama-3.1-8b-instant"
    
    # LLM Parameters
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    timeout_seconds: int = 15
    
    # Retry Configuration
    max_retries: int = 2
    retry_delay_seconds: float = 1.0
    
    # Output Parsing
    json_parse_timeout: int = 5  # seconds
    fallback_on_parse_error: bool = True
    
    # Token Budget (for cost tracking)
    max_tokens_per_request: int = 2000
    token_cost_per_1k: float = 0.05  # Groq pricing estimate
    
    def __post_init__(self) -> None:
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
    
    @property
    def cost_per_request(self) -> float:
        """Estimate cost per request in USD"""
        return (self.max_tokens_per_request / 1000) * self.token_cost_per_1k
