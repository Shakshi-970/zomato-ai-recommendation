"""Run Phase 4: LLM Recommendation demo / test suite."""
import sys
import json
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from src.phase2.models import StandardizedPreference
from src.phase4.config import Phase4Config
from src.phase4.service import LLMOrchestrator

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

config = Phase4Config()
orchestrator = LLMOrchestrator(config=config)

SAMPLE_CANDIDATES = [
    {"restaurant_id": "101", "name": "Bella Italia", "cuisines": "Italian, Pizza",
     "city": "Bangalore", "locality": "Koramangala", "rating": 4.4,
     "avg_cost_for_two": 1200, "votes": 850, "final_score": 0.91},
    {"restaurant_id": "102", "name": "The Pasta House", "cuisines": "Italian, Continental",
     "city": "Bangalore", "locality": "Indiranagar", "rating": 4.1,
     "avg_cost_for_two": 1100, "votes": 620, "final_score": 0.87},
    {"restaurant_id": "103", "name": "Pizza Roma", "cuisines": "Pizza, Italian",
     "city": "Bangalore", "locality": "Whitefield", "rating": 3.9,
     "avg_cost_for_two": 800, "votes": 430, "final_score": 0.80},
    {"restaurant_id": "104", "name": "Spice Garden", "cuisines": "North Indian, Mughlai",
     "city": "Bangalore", "locality": "HSR Layout", "rating": 4.2,
     "avg_cost_for_two": 900, "votes": 1100, "final_score": 0.72},
    {"restaurant_id": "105", "name": "Trattoria Verdi", "cuisines": "Italian, Desserts",
     "city": "Bangalore", "locality": "MG Road", "rating": 4.5,
     "avg_cost_for_two": 1500, "votes": 990, "final_score": 0.89},
]


def print_header(title):
    print(f"\n{'='*70}\n  {title}\n{'='*70}")


def print_response(response):
    print(f"\n  Query ID : {response.query_id}")
    print(f"  Model    : {response.llm_model}")
    print(f"  Tokens   : {response.tokens_used}  |  Cost: ${response.cost_usd:.4f}")
    print(f"  Summary  : {response.summary}")
    print("\n  Recommendations:")
    for rec in response.recommendations:
        print(f"    [{rec.rank}] {rec.name} | {rec.cuisine} | "
              f"Rating: {rec.rating} | Cost: ₹{rec.estimated_cost}")
        print(f"         {rec.explanation}")


def main():
    print_header("TEST 1: Italian / Medium Budget / Bangalore")
    pref = StandardizedPreference(
        location="Bangalore", budget_tier="medium",
        preferred_cuisines=["Italian", "Pizza"], min_rating=3.5,
        additional_preferences=["family-friendly"], top_k=3,
    )
    res = orchestrator.recommend(preference=pref.model_dump(), candidates=SAMPLE_CANDIDATES, top_k=3)
    print_response(res)
    assert res.parse_success and len(res.recommendations) == 3
    print("\n✅ TEST 1 PASSED")


if __name__ == "__main__":
    main()
