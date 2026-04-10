"""
Streamlit entrypoint for Streamlit Cloud deployment.

Streamlit Cloud requires a `streamlit run` entrypoint. This file:
1. Loads the GROQ_API_KEY from Streamlit secrets into the environment.
2. Starts the FastAPI server (uvicorn) in a background daemon thread.
3. Displays a simple status dashboard so the Streamlit app is not blank.

The FastAPI backend is accessible at the same host on port 8080.
"""

import os
import threading
import time

import streamlit as st

# ── Inject secrets into environment before importing the app ───────────────
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

import uvicorn
from run_phase5_api import app  # noqa: E402  (must come after secret injection)

# ── Start FastAPI in a background thread (runs once per process) ───────────
_server_started = False

def _run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="warning")

if not _server_started:
    thread = threading.Thread(target=_run_server, daemon=True)
    thread.start()
    _server_started = True
    time.sleep(2)  # Give uvicorn a moment to bind

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
col2.metric("Port", "8080")

st.markdown("---")
st.markdown("### Available Endpoints")

endpoints = {
    "`POST /auth/register`": "Register a new user",
    "`POST /auth/login`": "Login with existing credentials",
    "`GET  /auth/me`": "Get current user from token",
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
