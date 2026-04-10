from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Phase3Config:
    data_file: Path = Path("data/processed/restaurants_clean.csv")
    scoring_file: Path = Path("src/phase3/scoring_config.json")
    llm_provider: str = "groq"
    candidate_cache_ttl_seconds: int = 300

    @property
    def groq_api_key(self) -> str:
        load_dotenv()
        return os.getenv("GROQ_API_KEY", "")

    def load_scoring(self) -> dict:
        return json.loads(self.scoring_file.read_text(encoding="utf-8"))

