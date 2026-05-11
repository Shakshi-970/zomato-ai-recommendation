from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path

# When a Postgres connection string is present (Vercel Postgres / Neon)
# we persist to the database; otherwise we use JSON files so local dev
# does not require a database. Vercel auto-injects POSTGRES_URL when a
# Postgres store is connected to the project.
_PG_URL = (
    os.environ.get("POSTGRES_URL")
    or os.environ.get("DATABASE_URL")
    or os.environ.get("POSTGRES_PRISMA_URL")
)
_USE_POSTGRES = bool(_PG_URL)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


if _USE_POSTGRES:
    # ── Postgres backend (Vercel / Neon) ──────────────────────────────────
    import psycopg

    _SCHEMA_READY = False

    def _connect():
        # prepare_threshold=None disables auto-prepared statements, which
        # are incompatible with pgbouncer's transaction-pooling mode used
        # by Vercel Postgres.
        return psycopg.connect(_PG_URL, autocommit=True, prepare_threshold=None)

    def _ensure_schema() -> None:
        global _SCHEMA_READY
        if _SCHEMA_READY:
            return
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    email    TEXT PRIMARY KEY,
                    name     TEXT NOT NULL,
                    password TEXT NOT NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    name  TEXT NOT NULL
                )
                """
            )
        _SCHEMA_READY = True

    def register(name: str, email: str, password: str) -> dict:
        _ensure_schema()
        email_norm = email.lower()
        name_clean = name.strip()
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email_norm,))
            if cur.fetchone():
                raise ValueError("Email is already registered. Please log in.")
            cur.execute(
                "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)",
                (email_norm, name_clean, _hash(password)),
            )
            token = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO sessions (token, email, name) VALUES (%s, %s, %s)",
                (token, email_norm, name_clean),
            )
        return {"name": name_clean, "email": email_norm, "token": token}

    def login(email: str, password: str) -> dict:
        _ensure_schema()
        email_norm = email.lower()
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT name, password FROM users WHERE email = %s",
                (email_norm,),
            )
            row = cur.fetchone()
            if not row or row[1] != _hash(password):
                raise ValueError("Invalid email or password.")
            user_name = row[0]
            token = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO sessions (token, email, name) VALUES (%s, %s, %s)",
                (token, email_norm, user_name),
            )
        return {"name": user_name, "email": email_norm, "token": token}

    def get_user(token: str) -> dict | None:
        _ensure_schema()
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT name, email FROM sessions WHERE token = %s",
                (token,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {"name": row[0], "email": row[1]}

else:
    # ── Local JSON fallback (development only) ────────────────────────────
    _DATA_DIR = Path(__file__).resolve().parents[2] / "data"
    USERS_FILE = _DATA_DIR / "users.json"
    SESSIONS_FILE = _DATA_DIR / "sessions.json"

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

    _sessions: dict[str, dict] = _load_sessions()

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
