# Source Layout

Code is organized phase-wise:

- `src/phase1/` - Data ingestion, preprocessing, schema validation, and reporting
- `src/phase2/` - Preference validation API, normalization, and service layer
- `src/phase3/` - Candidate retrieval, pre-ranking, caching, and Groq input prep

Phase-specific run entry points:

- `python -m src.phase1.run`
- `python -m src.phase2.run_api`
- `python -m src.phase2.run_demo`
- `python -m src.phase3.run_api`
- `python -m src.phase3.run_demo`

Backward-compatible root wrappers are retained:

- `run_phase1.py`
- `run_phase2_api.py`
- `run_phase2_demo.py`
- `run_phase3_api.py`
- `run_phase3_demo.py`

