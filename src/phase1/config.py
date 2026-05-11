from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation"
    split: str = "train"
    root: Path = Path(".")

    @property
    def data_raw_dir(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def data_processed_dir(self) -> Path:
        return self.root / "data" / "processed"

    @property
    def reports_dir(self) -> Path:
        return self.root / "reports"

    @property
    def raw_parquet(self) -> Path:
        return self.data_raw_dir / "zomato_raw.parquet"

    @property
    def processed_parquet(self) -> Path:
        return self.data_processed_dir / "restaurants_clean.parquet"

    @property
    def processed_csv(self) -> Path:
        return self.data_processed_dir / "restaurants_clean.csv"

    @property
    def quality_report_json(self) -> Path:
        return self.reports_dir / "phase1_data_quality_report.json"

    @property
    def quality_report_md(self) -> Path:
        return self.reports_dir / "phase1_data_quality_report.md"

    def ensure_dirs(self) -> None:
        self.data_raw_dir.mkdir(parents=True, exist_ok=True)
        self.data_processed_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

