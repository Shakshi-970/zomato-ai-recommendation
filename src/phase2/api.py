from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .models import PreferenceValidationRequest
from .service import PreferenceService


app = FastAPI(title="Restaurant Recommendation - Phase 2 API", version="1.0.0")
service = PreferenceService(
    known_cities_file=Path("data/processed/restaurants_clean.csv"),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/preferences/validate")
def validate_preferences(request: PreferenceValidationRequest) -> JSONResponse:
    result = service.validate_and_normalize(request)
    status_code = 200 if result.valid else 400
    return JSONResponse(status_code=status_code, content=result.model_dump())

