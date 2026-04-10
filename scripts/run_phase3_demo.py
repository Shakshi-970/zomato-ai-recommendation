"""Run Phase 3: Candidate Retrieval demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.phase3.run_demo import main

if __name__ == "__main__":
    main()
