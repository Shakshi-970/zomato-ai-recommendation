# Phase 1 Implementation Guide

## What is implemented
- Data ingestion from Hugging Face dataset: `ManikaSaini/zomato-restaurant-recommendation`
- Raw dataset persistence to `data/raw/zomato_raw.parquet`
- Canonical schema mapping and normalization for key fields:
  - `restaurant_id`, `name`, `city`, `locality`, `cuisines`, `avg_cost_for_two`, `currency`, `rating`, `votes`
- Data cleaning:
  - null handling
  - numeric parsing
  - rating and cost clipping
  - deduplication
- Schema validation report
- Processed outputs and quality reports

## Run instructions
```bash
python -m pip install -r requirements.txt
python run_phase1.py
```

## Output artifacts
- `data/raw/zomato_raw.parquet`
- `data/processed/restaurants_clean.parquet`
- `data/processed/restaurants_clean.csv`
- `reports/phase1_data_quality_report.json`
- `reports/phase1_data_quality_report.md`

## Notes
- Column mapping is alias-based and resilient to minor source column naming changes.
- If dataset schema changes significantly, update alias mappings in `src/phase1/pipeline.py`.
