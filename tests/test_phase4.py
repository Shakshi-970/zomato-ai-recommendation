"""Phase 4 integration tests — LLM Recommendation Orchestration."""
import sys
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.phase2.models import StandardizedPreference
from src.phase4.service import LLMOrchestrator, Phase4Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
orchestrator = LLMOrchestrator(config=Phase4Config())


def print_result(label, result):
    print(f"\n{'='*60}\n  {label}\n{'='*60}")
    print(f"  Query ID      : {result.query_id}")
    print(f"  Parse success : {result.parse_success}  |  Fallback: {result.fallback_used}")
    print(f"  Summary       : {result.summary}")
    for r in result.recommendations:
        print(f"    [{r.rank}] {r.name} | {r.cuisine} | Rating: {r.rating} | Cost: ₹{r.estimated_cost}")
        print(f"         {r.explanation}")


def test_case_1_italian_bangalore():
    print("\n[TC1] Italian / Medium Budget / Bangalore")
    pref = StandardizedPreference(
        location="Bangalore", budget_tier="medium",
        preferred_cuisines=["Italian", "Pizza"], min_rating=3.5,
        additional_preferences=["family-friendly"], top_k=3,
    )
    candidates = [
        {"restaurant_id": "101", "name": "Bella Italia", "cuisines": "Italian, Pizza",
         "rating": 4.4, "avg_cost_for_two": 1200, "locality": "Koramangala", "city": "Bangalore", "votes": 850, "pre_rank_score": 0.91},
        {"restaurant_id": "102", "name": "The Pasta House", "cuisines": "Italian, Continental",
         "rating": 4.1, "avg_cost_for_two": 1100, "locality": "Indiranagar", "city": "Bangalore", "votes": 620, "pre_rank_score": 0.87},
        {"restaurant_id": "103", "name": "Pizza Roma", "cuisines": "Pizza, Italian",
         "rating": 3.9, "avg_cost_for_two": 800, "locality": "Whitefield", "city": "Bangalore", "votes": 430, "pre_rank_score": 0.80},
        {"restaurant_id": "104", "name": "Spice Garden", "cuisines": "North Indian, Mughlai",
         "rating": 4.2, "avg_cost_for_two": 900, "locality": "HSR Layout", "city": "Bangalore", "votes": 1100, "pre_rank_score": 0.72},
        {"restaurant_id": "105", "name": "Trattoria Verdi", "cuisines": "Italian, Desserts",
         "rating": 4.5, "avg_cost_for_two": 1500, "locality": "MG Road", "city": "Bangalore", "votes": 990, "pre_rank_score": 0.89},
    ]
    result = orchestrator.recommend(pref, candidates, top_k=3)
    print_result("TC1 - Italian / Medium / Bangalore", result)
    assert result.parse_success and len(result.recommendations) == 3
    print("[PASS] TC1")


def test_case_2_chinese_mumbai():
    print("\n[TC2] Chinese / Low Budget / Mumbai")
    pref = StandardizedPreference(
        location="Mumbai", budget_tier="low",
        preferred_cuisines=["Chinese", "Asian"], min_rating=3.0,
        additional_preferences=["quick service"], top_k=3,
    )
    candidates = [
        {"restaurant_id": "201", "name": "Wok Express", "cuisines": "Chinese, Asian",
         "rating": 3.9, "avg_cost_for_two": 400, "locality": "Andheri", "city": "Mumbai", "votes": 720, "pre_rank_score": 0.85},
        {"restaurant_id": "202", "name": "Dragon Bowl", "cuisines": "Chinese, Thai",
         "rating": 4.0, "avg_cost_for_two": 500, "locality": "Bandra", "city": "Mumbai", "votes": 540, "pre_rank_score": 0.82},
        {"restaurant_id": "203", "name": "Golden Chopsticks", "cuisines": "Chinese",
         "rating": 3.5, "avg_cost_for_two": 350, "locality": "Dadar", "city": "Mumbai", "votes": 310, "pre_rank_score": 0.75},
    ]
    result = orchestrator.recommend(pref, candidates, top_k=3)
    print_result("TC2 - Chinese / Low / Mumbai", result)
    valid_ids = {str(c["restaurant_id"]) for c in candidates}
    for r in result.recommendations:
        assert r.restaurant_id in valid_ids, f"Hallucinated ID: {r.restaurant_id}"
    print("[PASS] TC2")


def test_case_3_fine_dining_delhi():
    print("\n[TC3] Fine Dining / High Budget / Delhi")
    pref = StandardizedPreference(
        location="Delhi", budget_tier="high",
        preferred_cuisines=["Continental", "French"], min_rating=4.0,
        additional_preferences=["fine dining", "romantic"], top_k=3,
    )
    candidates = [
        {"restaurant_id": "301", "name": "Le Meridien Bistro", "cuisines": "French, Continental",
         "rating": 4.7, "avg_cost_for_two": 4000, "locality": "Connaught Place", "city": "Delhi", "votes": 1200, "pre_rank_score": 0.97},
        {"restaurant_id": "302", "name": "Chez Pierre", "cuisines": "French, European",
         "rating": 4.5, "avg_cost_for_two": 3500, "locality": "Defence Colony", "city": "Delhi", "votes": 870, "pre_rank_score": 0.93},
        {"restaurant_id": "303", "name": "The Oberoi Grill", "cuisines": "Continental, Steakhouse",
         "rating": 4.6, "avg_cost_for_two": 5000, "locality": "Chanakyapuri", "city": "Delhi", "votes": 1500, "pre_rank_score": 0.95},
    ]
    result = orchestrator.recommend(pref, candidates, top_k=3)
    print_result("TC3 - Fine Dining / High / Delhi", result)
    valid_ids = {str(c["restaurant_id"]) for c in candidates}
    for r in result.recommendations:
        assert r.restaurant_id in valid_ids, f"Hallucinated ID: {r.restaurant_id}"
    print("[PASS] TC3")


if __name__ == "__main__":
    print(f"\n[START] Phase 4 Test Suite  |  Model: {Phase4Config().model}")
    test_case_1_italian_bangalore()
    test_case_2_chinese_mumbai()
    test_case_3_fine_dining_delhi()
    print("\n[DONE] All tests passed!")
