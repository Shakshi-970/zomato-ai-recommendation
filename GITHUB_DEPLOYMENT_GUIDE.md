# GitHub & Vercel Deployment Guide

## Part 1: Push to GitHub

### Step 1: Create a GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click **"+"** → **"New repository"**
3. Name it: `zomato-ai-recommendation` (or your preferred name)
4. Choose **Public** or **Private**
5. Do NOT initialize with README, .gitignore, or license (you already have them)
6. Click **Create repository**

### Step 2: Connect Local Repository to GitHub
Run these commands in your project root directory:

```bash
# View current remote (should show nothing if first time)
git remote -v

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/zomato-ai-recommendation.git

# Verify remote was added
git remote -v
```

### Step 3: Check Git Status & Commit
```bash
# See what's staged/unstaged
git status

# Stage all changes
git add .

# Commit your work
git commit -m "Initial commit: Zomato AI recommendation system with Phase 5 API, Next.js frontend, and auth"

# Check the log to verify
git log --oneline -n 5
```

### Step 4: Push to GitHub
```bash
# Push to main branch (creates it if doesn't exist)
git branch -M main
git push -u origin main

# Verify in browser: https://github.com/YOUR_USERNAME/zomato-ai-recommendation
```

---

## Part 2: Backend Deployment

### Option A: Deploy on Render (Recommended for FastAPI)

1. **Sign up**: Go to [Render.com](https://render.com) and sign in with GitHub
2. **Create Web Service**:
   - Click **"New +"** → **"Web Service"**
   - Select your GitHub repository
   - Connect Render to GitHub if prompted
3. **Configure**:
   - **Name**: `zomato-ai-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn run_phase5_api:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: Set in Dashboard:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```
5. **Deploy**: Click **"Create Web Service"** and wait for deployment

**Your Backend URL**: `https://zomato-ai-api.onrender.com`

### Option B: Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Configure:
   - **Root Directory**: `.` (current)
   - **Add Variable**: `GROQ_API_KEY` with your Groq API key
5. Railway auto-detects Python and deploys

### Option C: Deploy on Vercel (Python Support)

1. Go to [Vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import your GitHub repository
4. **Root Directory**: `.`
5. **Build Command**: `pip install -r requirements.txt`
6. **Output Directory**: (leave blank)
7. **Add Environment Variables**:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```
8. Deploy

---

## Part 3: Frontend Deployment on Vercel

### Step 1: Deploy Frontend on Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import your GitHub repository
4. **Configure**:
   - **Framework**: Next.js (auto-detected)
   - **Root Directory**: `frontend-nextjs`
   - **Build Command**: `npm run build` (auto-filled)
   - **Install Command**: `npm install` (auto-filled)
5. **Environment Variables**: Add these:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url
   ```
   Example: `https://zomato-ai-api.onrender.com`

### Step 2: Update Frontend API Calls

Edit [frontend-nextjs/components/PreferenceForm.tsx](../frontend-nextjs/components/PreferenceForm.tsx) and ensure API calls use the environment variable:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860';

// In your API calls:
const response = await axios.post(`${API_URL}/api/recommendations`, data);
```

### Step 3: Deploy

Click **"Deploy"** and wait for Vercel to build and deploy your Next.js app.

**Your Frontend URL**: `https://your-project-name.vercel.app`

---

## Part 4: Post-Deployment Checklist

### Backend Checks
- [ ] Backend API is running: Visit `https://your-backend-url/docs` (Swagger UI)
- [ ] Test endpoint: `POST /api/recommendations` with sample data
- [ ] Environment variables are set correctly
- [ ] CORS is configured for your frontend URL

### Frontend Checks
- [ ] Frontend loads without errors
- [ ] API calls connect to the backend (check Network tab in DevTools)
- [ ] Recommendation form works end-to-end
- [ ] No CORS errors in console

### Git Checks
- [ ] All code is committed and pushed to `main` branch
- [ ] `.env` file is in `.gitignore` (secrets not exposed)
- [ ] `node_modules/` and `__pycache__/` are ignored

---

## Part 5: Environment Variables Setup

### Backend (.env file - DO NOT COMMIT)
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### Frontend (.env.local - DO NOT COMMIT)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url
```

In Vercel Dashboard:
1. Project Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL` with your backend URL

---

## Troubleshooting

### Backend Won't Start
- Check Render/Railway/Vercel logs: `git clone` your repo and run locally first
- Verify `requirements.txt` has all dependencies: `pip install -r requirements.txt`
- Test locally: `uvicorn run_phase5_api:app --reload`

### Frontend Can't Reach Backend
- Verify backend URL in environment variable
- Check CORS configuration in `run_phase5_api.py`
- Open DevTools Network tab and see actual request/response

### CORS Errors
In your `run_phase5_api.py`, ensure CORS is set to accept your frontend:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Quick Reference: Command Cheatsheet

```bash
# Check Git status
git status

# Stage and commit
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline -n 10

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push your code with `git push -u origin main`
3. ✅ Deploy backend on Render/Railway
4. ✅ Deploy frontend on Vercel
5. ✅ Update environment variables in deployment platforms
6. ✅ Test end-to-end functionality
7. ✅ Monitor logs for errors

**Your deployed system will be live at your Vercel frontend URL!**
