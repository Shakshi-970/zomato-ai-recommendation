from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


DICTIONARY_DIR = Path(__file__).resolve().parent / "dictionaries"


def _load_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache
def budget_aliases() -> dict[str, str]:
    return _load_json(DICTIONARY_DIR / "budget_aliases.json")


@lru_cache
def preference_aliases() -> dict[str, str]:
    return _load_json(DICTIONARY_DIR / "preference_aliases.json")


@lru_cache
def city_aliases() -> dict[str, str]:
    return _load_json(DICTIONARY_DIR / "city_aliases.json")

