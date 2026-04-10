"""Comprehensive Groq LLM functionality tests for Phase 4."""
import os
import sys
import json
import time
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("GROQ_API_KEY is not set.")

client = Groq(api_key=api_key)
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

CANDIDATES = [
    {"restaurant_id": "101", "name": "Bella Italia", "cuisines": "Italian, Pizza",
     "rating": 4.4, "avg_cost_for_two": 1200, "locality": "Koramangala", "votes": 850},
    {"restaurant_id": "102", "name": "The Pasta House", "cuisines": "Italian, Continental",
     "rating": 4.1, "avg_cost_for_two": 1100, "locality": "Indiranagar", "votes": 620},
    {"restaurant_id": "103", "name": "Pizza Roma", "cuisines": "Pizza, Italian",
     "rating": 3.9, "avg_cost_for_two": 800, "locality": "Whitefield", "votes": 430},
    {"restaurant_id": "104", "name": "Spice Garden", "cuisines": "North Indian, Mughlai",
     "rating": 4.2, "avg_cost_for_two": 900, "locality": "HSR Layout", "votes": 1100},
]


def header(title):
    print(f"\n{'='*70}\n  {title}\n{'='*70}")


def test_1_basic_ranking():
    header("TEST 1: Basic Ranking")
    prompt = (
        "Rank these 4 restaurants for Italian food, medium budget (₹1000-1500) in Bangalore:\n"
        "1. Bella Italia - Italian | 4.4★ | ₹1200\n"
        "2. The Pasta House - Italian | 4.1★ | ₹1100\n"
        "3. Pizza Roma - Pizza | 3.9★ | ₹800\n"
        "4. Spice Garden - North Indian | 4.2★ | ₹900\n"
        "Provide a ranked list with 2-3 sentence reasons."
    )
    res = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    print(res.choices[0].message.content)
    print("\n✅ TEST 1 PASSED")
    return True


def test_2_json_output():
    header("TEST 2: JSON Output Parsing")
    prompt = (
        "Select the top 2 Italian restaurants and return ONLY valid JSON (no markdown):\n"
        "- Bella Italia (ID: 101, Rating: 4.4, Cost: ₹1200)\n"
        "- The Pasta House (ID: 102, Rating: 4.1, Cost: ₹1100)\n"
        "- Pizza Roma (ID: 103, Rating: 3.9, Cost: ₹800)\n\n"
        '{"recommendations":[{"rank":1,"restaurant_id":"...","name":"...","reason":"..."}],"summary":"..."}'
    )
    res = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    raw = res.choices[0].message.content
    parsed = json.loads(raw)
    assert "recommendations" in parsed and len(parsed["recommendations"]) > 0
    print(json.dumps(parsed, indent=2))
    print("\n✅ TEST 2 PASSED")
    return True


def test_3_full_flow():
    header("TEST 3: Full Recommendation Flow")
    candidate_text = "\n".join(
        f"- {r['name']} (ID: {r['restaurant_id']}, Rating: {r['rating']}, "
        f"Cost: ₹{r['avg_cost_for_two']}, Cuisines: {r['cuisines']})"
        for r in CANDIDATES
    )
    prompt = (
        f"Recommend top 3 Italian restaurants (medium budget, Bangalore):\n{candidate_text}\n\n"
        'Return ONLY JSON: {"recommendations":[{"rank":1,"restaurant_id":"...","name":"...",'
        '"cuisines":"...","rating":0,"estimated_cost":0,"explanation":"..."}],"summary":"..."}'
    )
    res = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    parsed = json.loads(res.choices[0].message.content)
    assert len(parsed["recommendations"]) == 3
    print(json.dumps(parsed, indent=2))
    print("\n✅ TEST 3 PASSED")
    return True


def test_4_speed():
    header("TEST 4: Response Speed")
    start = time.time()
    res = client.chat.completions.create(
        messages=[{"role": "user", "content": "Best Italian restaurant from: Bella Italia (4.4★), Pizza Roma (3.9★)? Reply in JSON: {\"top_pick\":{\"name\":\"...\",\"reason\":\"...\"}}"}],
        model="llama-3.1-8b-instant",
    )
    elapsed = time.time() - start
    print(f"Response time: {elapsed:.2f}s | Tokens: {res.usage.total_tokens}")
    assert elapsed < 5.0, f"Too slow: {elapsed:.2f}s"
    print("\n✅ TEST 4 PASSED")
    return True


if __name__ == "__main__":
    print(f"\n{'='*70}\n  GROQ LLM FUNCTIONALITY TEST SUITE\n{'='*70}")
    results = {
        "Test 1 - Basic Ranking": test_1_basic_ranking(),
        "Test 2 - JSON Output": test_2_json_output(),
        "Test 3 - Full Flow": test_3_full_flow(),
        "Test 4 - Speed": test_4_speed(),
    }
    passed = sum(results.values())
    print(f"\n{'='*70}")
    for name, ok in results.items():
        print(f"{'✅' if ok else '❌'} {name}")
    print(f"\nOverall: {passed}/{len(results)} passed\n{'='*70}")
