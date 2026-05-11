"""
Streamlit entrypoint for Streamlit Cloud deployment.

Starts the FastAPI/uvicorn server in a background thread once per process,
using a socket check to avoid 'address already in use' on Streamlit reruns.
"""

import os
import socket
import threading
import time

import streamlit as st

# ── Inject secrets into environment before importing the app ───────────────
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

import uvicorn
from run_phase5_api import app  # must come after secret injection

PORT = 8080


def _port_in_use(port: int) -> bool:
    """Return True if something is already listening on the port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def _run_server():
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")


# ── Start server only if not already running ──────────────────────────────
if not _port_in_use(PORT):
    thread = threading.Thread(target=_run_server, daemon=True)
    thread.start()
    time.sleep(2)  # give uvicorn time to bind

# ── Streamlit status dashboard ─────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato AI – Backend",
    page_icon="🍽️",
    layout="centered",
)

st.title("🍽️ Zomato AI Restaurant Recommendation")
st.subheader("Backend API Status")

col1, col2 = st.columns(2)
col1.metric("Status", "Running ✅")
col2.metric("Port", str(PORT))

st.markdown("---")
st.markdown("### Available Endpoints")

endpoints = {
    "`POST /auth/register`": "Register a new user",
    "`POST /auth/login`": "Login with existing credentials",
    "`GET  /auth/me`": "Verify session token",
    "`GET  /phase5/locations`": "List supported cities and localities",
    "`POST /phase5/recommend`": "Get AI-powered restaurant recommendations",
    "`GET  /phase5/health`": "Health check",
    "`GET  /docs`": "Interactive API documentation (Swagger UI)",
}

for endpoint, desc in endpoints.items():
    st.markdown(f"- {endpoint} — {desc}")

st.markdown("---")
st.info(
    "This page confirms the backend is running. "
    "The Next.js frontend (deployed on Vercel) communicates with this server via the REST API above."
)
