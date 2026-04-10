# Phase 3 Implementation Guide

## What is implemented
- Hard filter engine:
  - city exact match
  - min rating threshold
  - budget window by tier
- Heuristic pre-ranker with configurable weights:
  - cuisine match
  - rating score
  - budget fit
  - preference tag match
- Candidate cache (TTL-based in-memory).
- Candidate response schema.
- Groq-ready payload builder for Phase 4.

## Files
- `src/phase3/config.py`
- `src/phase3/scoring_config.json`
- `src/phase3/cache.py`
- `src/phase3/models.py`
- `src/phase3/service.py`
- `src/phase3/api.py`
- `src/phase3/run_api.py`
- `src/phase3/run_demo.py`

## API endpoints
- `GET /health`
- `POST /phase3/candidates`
- `POST /phase3/groq-input`

## Example request (`/phase3/candidates`)
```json
{
  "preference": {
    "location": "Bangalore",
    "budget_tier": "medium",
    "preferred_cuisines": ["Italian", "Chinese"],
    "min_rating": 4.0,
    "additional_preferences": ["quick service"],
    "top_k": 5
  },
  "candidate_pool_size": 20
}
```

## Run
```bash
python -m pip install -r requirements.txt
python run_phase3_api.py
```

Swagger:
- `http://127.0.0.1:8001/docs`

## Environment
- `.env` key used: `GROQ_API_KEY`
- Phase 3 does not call Groq yet, but marks whether API key is configured and prepares payload for Phase 4.
