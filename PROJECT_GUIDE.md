# Zomato AI Restaurant Recommendation System — Project Guide

A complete reference for understanding the codebase and answering interview questions confidently.

---

## Table of Contents

1. [What This Project Does](#1-what-this-project-does)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [How It Works — The 5-Phase Pipeline](#4-how-it-works--the-5-phase-pipeline)
5. [Authentication System](#5-authentication-system)
6. [Frontend Architecture](#6-frontend-architecture)
7. [API Endpoints](#7-api-endpoints)
8. [Deployment Architecture](#8-deployment-architecture)
9. [Data Flow — End to End](#9-data-flow--end-to-end)
10. [Key Interview Questions & Answers](#10-key-interview-questions--answers)

---

## 1. What This Project Does

A user tells the system:
- Which **city** and **locality** they're in
- What **cuisine** they want (e.g., North Indian, Chinese)
- Their **budget** (cheap / moderate / expensive)
- Minimum **rating** they expect (1–4 stars)
- Whether they prefer **dine-in or delivery**

The system returns **AI-ranked restaurant recommendations** with a natural-language explanation for why each one was picked.

---

## 2. Tech Stack

### Backend
| Tool | Purpose |
|------|---------|
| **FastAPI** | REST API framework (Python) |
| **Groq API** | LLM inference (llama-3.1-8b-instant model) |
| **Pandas** | Data loading and filtering |
| **Pydantic** | Request/response validation |
| **Uvicorn** | ASGI server to run FastAPI |
| **Python-dotenv** | Load environment variables from `.env` |

### Frontend
| Tool | Purpose |
|------|---------|
| **Next.js 14** | React framework with App Router |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first CSS styling |
| **Axios** | HTTP client for API calls |
| **React Context API** | Global auth state management |

### Infrastructure
| Tool | Purpose |
|------|---------|
| **Vercel** | Hosts both frontend and backend |
| **GitHub** | Source code repository |

---

## 3. Project Structure

```
M1/
├── src/                        ← All backend business logic
│   ├── auth/                   ← Login, register, session management
│   ├── phase1/                 ← Data cleaning pipeline
│   ├── phase2/                 ← User preference validation
│   ├── phase3/                 ← Restaurant filtering & scoring
│   ├── phase4/                 ← LLM ranking via Groq
│   └── phase5/                 ← End-to-end orchestrator
│
├── api/
│   └── index.py                ← Vercel serverless entry point
│
├── frontend-nextjs/            ← Next.js React app
│   ├── app/                    ← Pages (App Router)
│   │   ├── page.tsx            ← Home (recommendation form)
│   │   └── login/page.tsx      ← Login / Register
│   ├── components/             ← Reusable UI components
│   └── context/AuthContext.tsx ← Global auth state
│
├── data/
│   ├── processed/
│   │   └── restaurants_clean.csv  ← Cleaned restaurant dataset
│   ├── users.json              ← Registered users (hashed passwords)
│   └── sessions.json           ← Active login sessions
│
├── run_phase5_api.py           ← FastAPI app factory (main server)
├── requirements.txt            ← Python dependencies
└── .env                        ← GROQ_API_KEY (not committed to git)
```

---

## 4. How It Works — The 5-Phase Pipeline

### Phase 1 — Data Ingestion & Cleaning

**What it does:** Takes raw Zomato restaurant data and produces a clean CSV.

**Key operations:**
- Normalizes cuisine names (e.g., "north indian" → "North Indian")
- Converts costs to a standard format
- Removes duplicates
- Validates required columns exist

**Output:** `data/processed/restaurants_clean.csv`

**When does it run?** Only once as a setup step. The cleaned CSV is committed and used by the API directly — no re-processing at runtime.

---

### Phase 2 — Preference Validation

**What it does:** Takes the user's raw input and validates/standardizes it.

**Example:**
- User types "mumbai" → normalizes to "Mumbai"
- User types "chinese food" → normalizes to "Chinese"
- User types "cheap" → normalizes to budget tier

**How it works:**
- Uses alias dictionaries (`src/phase2/dictionaries/`) — JSON files mapping hundreds of spelling variations to canonical forms
- PreferenceService checks if city/locality exists in the dataset

**Why it matters:** Prevents garbage input from reaching the filtering stage.

---

### Phase 3 — Candidate Retrieval

**What it does:** Filters the cleaned CSV to find restaurants matching the user's criteria.

**Filtering steps:**
1. Filter by city and locality
2. Filter by budget range
3. Filter by minimum rating
4. Filter by dining type (dine-in / delivery)
5. Filter by cuisine(s)
6. **Score** remaining restaurants by a weighted formula
7. Return top N candidates (e.g., top 20)

**Scoring weights** are in `src/phase3/scoring_config.json` — allows tuning without changing code.

**Output:** A list of candidate restaurants with their scores.

---

### Phase 4 — LLM Ranking

**What it does:** Takes the Phase 3 candidates and asks Groq's LLM to rank them intelligently and explain why.

**How it works:**
1. `prompts.py` builds a structured prompt containing:
   - User's preferences
   - List of candidate restaurants (name, cuisine, rating, cost, reviews)
2. Sends the prompt to Groq API (model: `llama-3.1-8b-instant`)
3. `parser.py` parses the JSON response from the LLM
4. Returns ranked restaurants with natural-language explanations

**Why LLM instead of just sorting?** The LLM can reason about combinations — "this restaurant is slightly above your budget but has exceptional reviews for the exact cuisine you want."

---

### Phase 5 — End-to-End Orchestrator

**What it does:** Ties Phases 2, 3, and 4 into a single API call.

**Flow:**
```
User input → Phase 2 (validate) → Phase 3 (filter) → Phase 4 (LLM rank) → Response
```

**Key endpoints:**
- `GET /phase5/locations` — returns all cities and their localities
- `POST /phase5/recommend` — runs the full pipeline
- `GET /phase5/health` — checks if API is running

---

## 5. Authentication System

### How it works

**Registration (`POST /auth/register`):**
1. Receives username + password
2. Hashes the password using SHA-256
3. Saves user to `data/users.json`
4. Returns a session token (random UUID)
5. Saves token → username mapping to `data/sessions.json`

**Login (`POST /auth/login`):**
1. Looks up the username in `data/users.json`
2. Hashes the submitted password and compares
3. If match → creates a new session token → saves to `data/sessions.json`
4. Returns the token

**Auth check (`GET /auth/me`):**
- Frontend sends `Authorization: Bearer <token>` header
- Backend checks if token exists in `sessions.json`
- Returns user info if valid, 401 if not

### Session Persistence

Sessions are stored in `data/sessions.json` (on disk), not just in memory. This means:
- Server restarts don't log users out
- Old sessions remain valid across deployments

### Frontend Auth Flow

- On login → token saved to `localStorage`
- On every page load → `AuthContext.tsx` calls `/auth/me` to verify the token is still valid
- If token rejected → clear `localStorage`, redirect to login
- All API calls include the token in the `Authorization` header

---

## 6. Frontend Architecture

### Next.js App Router

The app uses Next.js 14's **App Router** (not the older Pages Router).

```
app/
├── layout.tsx       ← Root layout, wraps everything with AuthProvider
├── page.tsx         ← Main page (shows recommendation form after login)
└── login/
    └── page.tsx     ← Login + Register form
```

### React Context for Auth

`AuthContext.tsx` provides:
- `user` — current logged-in user (or null)
- `token` — JWT-style session token
- `login(username, password)` — calls API, stores token
- `logout()` — clears token from localStorage
- `isLoading` — true while verifying token on page load

Any component can access auth state with `useAuth()` hook.

### Key Components

| Component | What it does |
|-----------|-------------|
| `Header.tsx` | Top nav bar — logo, city selector, user name, logout |
| `PreferenceForm.tsx` | The main form — city, locality, cuisine, budget, star rating |
| `RecommendationCard.tsx` | One restaurant result card — name, rating, cost, AI explanation |
| `RecommendationsContainer.tsx` | Grid of cards with loading and empty states |
| `SearchableDropdown.tsx` | Reusable dropdown with search/filter capability |

### Star Rating Feature

Built directly into `PreferenceForm.tsx` as an inline component:
- 4 stars (matching Zomato's 1–4 scale)
- Click a star to set rating, click same star again to deselect
- Hover preview (stars light up before you click)
- Shows helper text: "Showing restaurants rated X–4"

---

## 7. API Endpoints

### Authentication
| Method | Endpoint | What it does |
|--------|----------|-------------|
| POST | `/auth/register` | Create new account |
| POST | `/auth/login` | Login, get session token |
| GET | `/auth/me` | Verify token, get user info |

### Recommendations
| Method | Endpoint | What it does |
|--------|----------|-------------|
| GET | `/phase5/locations` | Get all cities + localities |
| POST | `/phase5/recommend` | Get AI restaurant recommendations |
| GET | `/phase5/health` | API health check |

### Request body for `/phase5/recommend`
```json
{
  "city": "Mumbai",
  "locality": "Bandra",
  "cuisines": ["North Indian", "Chinese"],
  "budget": "moderate",
  "min_rating": 3.5,
  "dining_type": "dine-in"
}
```

---

## 8. Deployment Architecture

### Why not Streamlit?

Streamlit Cloud was attempted first. It failed because:
- Streamlit only exposes **port 8501** (the Streamlit UI port)
- All other ports (like our FastAPI's 8080) are **blocked by their nginx proxy**
- There's no way to run a public REST API on Streamlit Cloud

### Why Vercel?

Vercel supports **Python Serverless Functions** — your FastAPI app runs as a serverless function automatically, no server management needed.

### How Backend Runs on Vercel

Vercel looks for `api/index.py` and runs it as a serverless function.

```python
# api/index.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from run_phase5_api import app   # Vercel picks up this `app` object
```

The `app` is a standard FastAPI ASGI app — Vercel knows how to serve it.

### Two Vercel Projects, One GitHub Repo

| Project | Root Directory | URL |
|---------|---------------|-----|
| Backend | `.` (repo root) | `https://zomato-ai-recommendation-rho.vercel.app` |
| Frontend | `frontend-nextjs/` | `https://zomato-ai-recommendation-llgh.vercel.app` |

### Environment Variables

- **Backend (Vercel):** `GROQ_API_KEY` set in Vercel dashboard → Settings → Environment Variables
- **Frontend (Vercel):** `NEXT_PUBLIC_API_URL=https://zomato-ai-recommendation-rho.vercel.app` set in Vercel dashboard

The `NEXT_PUBLIC_` prefix makes the variable available in the browser (client-side JavaScript).

---

## 9. Data Flow — End to End

```
User opens browser
        ↓
Next.js frontend loads (Vercel CDN)
        ↓
AuthContext checks localStorage for token
        ↓
Calls GET /auth/me on backend to validate token
        ↓ (if valid)
User sees recommendation form
        ↓
Frontend calls GET /phase5/locations → populates city/locality dropdowns
        ↓
User fills form → clicks "Get Recommendations"
        ↓
Frontend calls POST /phase5/recommend
        ↓
Backend Phase 5 Orchestrator runs:
  1. Phase 2: Validates & normalizes preferences
  2. Phase 3: Filters restaurants_clean.csv, scores, returns top 20
  3. Phase 4: Sends top 20 to Groq LLM for intelligent ranking
        ↓
Groq LLM returns ranked list + explanations
        ↓
Backend returns JSON response
        ↓
Frontend renders RecommendationCards
```

---

## 10. Key Interview Questions & Answers

### About the Project

**Q: What problem does this project solve?**
> Finding good restaurants is hard because simple filters (rating > 4, budget = cheap) don't understand context. This system combines traditional filtering with LLM reasoning to give personalized, explained recommendations.

**Q: Why did you use an LLM for ranking?**
> Traditional sorting by rating or price ignores combinations — a restaurant slightly above budget might be worth it if reviews specifically praise the cuisine the user wants. The LLM can reason about these trade-offs holistically and explain its reasoning in natural language.

---

### About the Architecture

**Q: Why a 5-phase pipeline instead of one big function?**
> Separation of concerns. Each phase has a single responsibility — validation, retrieval, ranking. This makes it easy to test each phase independently, swap implementations (e.g., change the LLM model), and debug failures (you know exactly which phase broke).

**Q: How does the LLM know about restaurants?**
> It doesn't have any pre-trained restaurant knowledge. We send the candidates directly in the prompt — their names, ratings, costs, and cuisine types. The LLM reasons over the data we provide, not its training data.

**Q: Why store sessions in a JSON file instead of a database?**
> For a prototype/demo project, a JSON file is simpler to set up with zero infrastructure. In production, you'd use Redis or a database for sessions. The key design principle (persist sessions on disk, not in memory) is the same.

---

### About FastAPI

**Q: Why FastAPI over Flask?**
> FastAPI provides automatic request validation via Pydantic, automatic API documentation at `/docs`, async support, and is faster than Flask. You define your request/response models once and get validation + docs for free.

**Q: What is Pydantic used for?**
> Pydantic validates incoming request data automatically. If a required field is missing or the wrong type, FastAPI returns a clear 422 error before your code even runs. It also serializes Python objects to JSON for responses.

**Q: What is an ASGI server?**
> ASGI (Asynchronous Server Gateway Interface) is the standard for async Python web apps. Uvicorn is the ASGI server that runs our FastAPI app — similar to how Gunicorn runs Flask apps.

---

### About Next.js

**Q: What is the App Router in Next.js 14?**
> App Router is Next.js's newer routing system where folders under `app/` define routes. `app/page.tsx` is the home page, `app/login/page.tsx` is `/login`. It supports React Server Components by default, though this project uses Client Components (marked with `"use client"`) since we need browser APIs like localStorage.

**Q: What is React Context?**
> React Context lets you share state across all components without passing props through every level. `AuthContext` stores the logged-in user and token — any component can call `useAuth()` to access it, whether it's the Header (to show username) or the form (to get the token for API calls).

**Q: What does `NEXT_PUBLIC_` mean in environment variables?**
> Next.js only exposes environment variables to the browser if they're prefixed with `NEXT_PUBLIC_`. Variables without this prefix are server-side only. Since our API URL needs to be used in browser JavaScript, it must have this prefix.

---

### About Deployment

**Q: How does Vercel run a FastAPI app?**
> Vercel supports Python Serverless Functions. Any file in the `api/` folder is automatically treated as a serverless function. We put `api/index.py` which imports our FastAPI `app` object. Vercel handles the ASGI interface, routing requests to our app.

**Q: What is a serverless function?**
> Instead of a server running 24/7, serverless functions are invoked on demand — a new instance spins up for each request, handles it, and shuts down. No server management, scales automatically, pay per request.

**Q: Why two separate Vercel projects from one GitHub repo?**
> The backend and frontend have different root directories and build processes. Vercel lets you specify the root directory per project — backend uses `.` (repo root) where `api/index.py` lives, frontend uses `frontend-nextjs/` where `package.json` lives.

---

### About Security

**Q: How are passwords stored?**
> Passwords are hashed using SHA-256 before storing in `users.json`. The raw password is never saved. During login, the submitted password is hashed and compared to the stored hash.

**Q: What is CORS and why is it configured?**
> CORS (Cross-Origin Resource Sharing) is a browser security policy that blocks requests from a different domain than the API. Since our frontend is at `vercel.app/frontend` and backend at `vercel.app/backend`, the browser would block calls without CORS headers. FastAPI's `CORSMiddleware` adds these headers to allow the frontend domain.

**Q: Why is `.env` in `.gitignore`?**
> The `.env` file contains `GROQ_API_KEY` — a secret API key. Committing it to GitHub would expose it publicly. Instead, the key is set directly in Vercel's environment variable settings.

---

### About the Data

**Q: Where does the restaurant data come from?**
> The raw data comes from a Zomato dataset (loaded from HuggingFace in Phase 1). It's cleaned once and saved as `restaurants_clean.csv`. The API reads this CSV at startup — no database needed for a prototype.

**Q: How does Phase 3 scoring work?**
> Each restaurant gets a weighted score based on: rating (highest weight), review count, match with requested cuisine, cost match to budget. Weights are configured in `scoring_config.json` so they can be tuned without changing code. Top-scoring restaurants are passed to the LLM.

---

*Built with FastAPI + Groq LLM (llama-3.1-8b-instant) + Next.js 14 + Tailwind CSS. Deployed on Vercel.*
