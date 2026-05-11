"""Run Phase 1: Data Engineering pipeline."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.phase1.run import main as phase1_main

if __name__ == "__main__":
    phase1_main()
