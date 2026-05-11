from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path

USERS_FILE    = Path(__file__).resolve().parents[2] / "data" / "users.json"
SESSIONS_FILE = Path(__file__).resolve().parents[2] / "data" / "sessions.json"


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── Users ──────────────────────────────────────────────────────────────────

def _load_users() -> dict:
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_users(users: dict) -> None:
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, indent=2), encoding="utf-8")


# ── Sessions (persisted to disk so server restarts don't log users out) ────

def _load_sessions() -> dict:
    if SESSIONS_FILE.exists():
        try:
            return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_sessions(sessions: dict) -> None:
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2), encoding="utf-8")


# In-memory cache loaded from disk at import time
_sessions: dict[str, dict] = _load_sessions()


# ── Public API ─────────────────────────────────────────────────────────────

def register(name: str, email: str, password: str) -> dict:
    users = _load_users()
    if email.lower() in users:
        raise ValueError("Email is already registered. Please log in.")
    users[email.lower()] = {
        "name": name.strip(),
        "email": email.lower(),
        "password": _hash(password),
    }
    _save_users(users)

    token = str(uuid.uuid4())
    _sessions[token] = {"name": name.strip(), "email": email.lower()}
    _save_sessions(_sessions)

    return {"name": name.strip(), "email": email.lower(), "token": token}


def login(email: str, password: str) -> dict:
    users = _load_users()
    user = users.get(email.lower())
    if not user or user["password"] != _hash(password):
        raise ValueError("Invalid email or password.")

    token = str(uuid.uuid4())
    _sessions[token] = {"name": user["name"], "email": email.lower()}
    _save_sessions(_sessions)

    return {"name": user["name"], "email": email.lower(), "token": token}


def get_user(token: str) -> dict | None:
    return _sessions.get(token)
