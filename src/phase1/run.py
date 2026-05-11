from pathlib import Path

from .config import PipelineConfig
from .pipeline import run_phase1


def main() -> None:
    config = PipelineConfig(root=Path("."))
    payload = run_phase1(config)
    schema = payload.get("schema_validation", {})

    print("Phase 1 completed successfully.")
    print(f"Raw records: {payload.get('raw_record_count')}")
    print(f"Clean records: {payload.get('clean_record_count')}")
    print(f"Pass rate: {schema.get('pass_rate')}%")
    print("Artifacts generated:")
    print("- data/raw/zomato_raw.parquet")
    print("- data/processed/restaurants_clean.parquet")
    print("- data/processed/restaurants_clean.csv")
    print("- reports/phase1_data_quality_report.json")
    print("- reports/phase1_data_quality_report.md")


if __name__ == "__main__":
    main()

