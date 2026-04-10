from src.phase2.models import StandardizedPreference

from .config import Phase3Config
from .service import CandidateRetrievalService


def main() -> None:
    service = CandidateRetrievalService(Phase3Config())
    pref = StandardizedPreference(
        location="Bangalore",
        budget_tier="medium",
        preferred_cuisines=["Italian", "Chinese"],
        min_rating=4.0,
        additional_preferences=["quick service"],
        top_k=5,
    )

    response = service.retrieve(pref, candidate_pool_size=20)
    groq_input = service.build_groq_input(pref, candidate_pool_size=10)

    print(
        {
            "total_after_filtering": response.total_after_filtering,
            "selected_count": response.selected_count,
            "top_candidate": response.candidates[0].model_dump() if response.candidates else None,
            "groq_input_rows": len(groq_input.candidate_table),
            "groq_api_key_configured": response.groq_api_key_configured,
        }
    )


if __name__ == "__main__":
    main()

