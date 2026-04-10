from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.phase2.models import StandardizedPreference

from .config import Phase3Config
from .models import CandidateRetrievalRequest
from .service import CandidateRetrievalService


app = FastAPI(title="Restaurant Recommendation - Phase 3 API", version="1.0.0")
service = CandidateRetrievalService(config=Phase3Config())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/phase3/candidates")
def get_candidates(request: CandidateRetrievalRequest) -> JSONResponse:
    result = service.retrieve(request.preference, request.candidate_pool_size)
    return JSONResponse(status_code=200, content=result.model_dump())


@app.post("/phase3/groq-input")
def get_groq_input(preference: StandardizedPreference) -> JSONResponse:
    result = service.build_groq_input(preference)
    return JSONResponse(status_code=200, content=result.model_dump())

