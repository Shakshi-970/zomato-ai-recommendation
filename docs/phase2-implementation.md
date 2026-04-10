# Phase 2 Implementation Guide

## What is implemented
- Preference validation and normalization layer.
- `POST /preferences/validate` endpoint (FastAPI).
- Normalization dictionaries for city, budget, and additional preferences.
- Internal standardized preference object for downstream retrieval.

## API details
- Endpoint: `POST /preferences/validate`
- Health check: `GET /health`

### Request payload
```json
{
  "location": "Bangalore",
  "budget_tier": "medium",
  "budget_for_two": 1500,
  "preferred_cuisines": ["Italian", "Chinese"],
  "min_rating": 4.0,
  "additional_preferences": ["family-friendly", "quick service"],
  "top_k": 5
}
```

### Response (valid request)
```json
{
  "valid": true,
  "errors": [],
  "normalized": {
    "location": "Bangalore",
    "budget_tier": "medium",
    "preferred_cuisines": ["Chinese", "Italian"],
    "min_rating": 4.0,
    "additional_preferences": ["family-friendly", "quick service"],
    "top_k": 5
  }
}
```

### Response (invalid request)
```json
{
  "valid": false,
  "errors": [
    "location is required and must map to a known city"
  ],
  "normalized": null
}
```

## Run instructions
```bash
python -m pip install -r requirements.txt
python run_phase2_api.py
```

Open Swagger docs at:
- `http://127.0.0.1:8000/docs`

## Dictionary files
- `src/phase2/dictionaries/budget_aliases.json`
- `src/phase2/dictionaries/city_aliases.json`
- `src/phase2/dictionaries/preference_aliases.json`
