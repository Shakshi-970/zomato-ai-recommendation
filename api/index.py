import sys
from pathlib import Path

# Make project root importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from run_phase5_api import app  # noqa: F401  — Vercel uses this as the ASGI entry point
