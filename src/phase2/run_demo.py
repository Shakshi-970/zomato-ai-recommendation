from pathlib import Path

from .models import PreferenceValidationRequest
from .service import PreferenceService


def main() -> None:
    service = PreferenceService(Path("data/processed/restaurants_clean.csv"))

    request = PreferenceValidationRequest(
        location="bengaluru",
        budget_tier="cheap",
        preferred_cuisines=["italian", " chinese "],
        min_rating=4.1,
        additional_preferences=["family friendly", "quick service"],
        top_k=5,
    )

    response = service.validate_and_normalize(request)
    print(response.model_dump())


if __name__ == "__main__":
    main()

