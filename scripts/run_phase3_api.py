"""Run Phase 3: Candidate Retrieval API server."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.phase3.run_api import main

if __name__ == "__main__":
    main()
