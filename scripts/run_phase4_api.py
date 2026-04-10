"""Run Phase 4: LLM Recommendation API server."""
import sys
import logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI
from uvicorn import run as uvicorn_run
from src.phase4.api import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def create_app():
    app = FastAPI(
        title="Phase 4: LLM-Powered Recommendation API",
        description="AI-powered restaurant recommendation using Groq LLM",
        version="1.0.0",
    )
    app.include_router(router)

    @app.get("/")
    def root():
        return {"message": "Phase 4 LLM Recommendation Service", "docs": "/docs"}

    return app


if __name__ == "__main__":
    logger.info("Starting Phase 4 API Server...")
    uvicorn_run(create_app(), host="127.0.0.1", port=8002, log_level="info")
