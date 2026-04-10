"""Phase 5 API Server - End-to-End Recommendation Service"""

import logging
from pathlib import Path
from dotenv import load_dotenv

# Load .env locally; on Vercel, env vars are injected via the dashboard
load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as uvicorn_run

from src.phase5.api import router
from src.auth.api import router as auth_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Zomato AI Restaurant Recommendation API",
        description="Complete workflow: Preference Validation → Candidate Retrieval → LLM Ranking",
        version="1.0.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Tighten to specific Vercel URL in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router)
    application.include_router(auth_router)

    @application.get("/")
    def root():
        return {
            "message": "Zomato AI Restaurant Recommendation Service",
            "docs": "/docs",
            "health": "/phase5/health",
        }

    return application


# Module-level `app` so uvicorn can reference it as `run_phase5_api:app`
app = create_app()


def main():
    """Run the API server locally."""
    logger.info("Starting Phase 5 End-to-End API Server...")
    uvicorn_run(
        "run_phase5_api:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    main()
