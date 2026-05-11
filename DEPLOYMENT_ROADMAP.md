# 🚀 Complete Deployment Roadmap

## Overview
Your Zomato AI Recommendation System is production-ready! Here's the complete path from local development to live deployment.

---

## 📊 Architecture After Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                         INTERNET                             │
└─────────────────────────────────────────────────────────────┘
          │                                        │
          ▼                                        ▼
    ┌──────────────┐                      ┌──────────────────┐
    │   Vercel     │                      │  Render/Railway  │
    │  Frontend    │  ◄──── API Calls ────►│  FastAPI Backend │
    │  Next.js     │   (HTTPS)            │  Python Service  │
    └──────────────┘                      └──────────────────┘
    Domain: your-app.vercel.app           Domain: your-api.onrender.com
                                          Endpoints: /docs, /api/recommendations
```

---

## 🎯 Step-by-Step Deployment Guide

### STEP 1: Prepare Your Repository (5 minutes)

```bash
# 1a. Navigate to project directory
cd "c:\Users\shakshi.d.singh\OneDrive - Accenture\zomato ai recommendation"

# 1b. Check git status
git status

# 1c. Stage all changes
git add .

# 1d. Commit with meaningful message
git commit -m "Production-ready: Zomato AI recommendation system with Phase 5 API, authentication, and Next.js frontend"

# 1e. Verify commit
git log --oneline -n 1
```

---

### STEP 2: Create GitHub Repository (3 minutes)

**On GitHub.com:**

1. Click **+** in top-right → **New repository**
2. Fill in:
   - **Repository name**: `zomato-ai-recommendation`
   - **Description**: `AI-powered restaurant recommendation system with FastAPI backend and Next.js frontend`
   - **Visibility**: Public (for portfolio) or Private (for confidentiality)
   - **DO NOT** initialize with README or .gitignore
3. Click **Create repository**

**In your terminal:**

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/zomato-ai-recommendation.git
git branch -M main
git push -u origin main

# Verify
git remote -v
```

**Expected output:**
```
origin  https://github.com/YOUR_USERNAME/zomato-ai-recommendation.git (fetch)
origin  https://github.com/YOUR_USERNAME/zomato-ai-recommendation.git (push)
```

---

### STEP 3: Deploy Backend (Choose ONE platform)

#### 🔵 **OPTION A: Render** (Easiest, Free Tier Available)

1. Go to [Render.com](https://render.com)
2. Sign in with GitHub (connect your account)
3. Click **"New"** → **"Web Service"**
4. Select your `zomato-ai-recommendation` repository
5. **Configuration**:
   - **Name**: `zomato-ai-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn run_phase5_api:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables** → Click **"Add Environment Variable"**:
   - **Key**: `GROQ_API_KEY`
   - **Value**: [Get from Groq console, paste here]
7. Click **"Create Web Service"**
8. Wait for build and deployment (5-10 minutes)
9. **Your backend URL**: `https://zomato-ai-api.onrender.com`

**Test it:**
```
Visit: https://zomato-ai-api.onrender.com/docs
You should see Swagger API documentation
```

---

#### 🟠 **OPTION B: Railway** (Modern, Good Performance)

1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub Repo"**
4. Select your repository
5. Railway auto-detects Python
6. **Add Variables**:
   - `GROQ_API_KEY` = [Your Groq API key]
7. Auto-deploys in ~2-3 minutes
8. **Your backend URL**: Check in Railway Dashboard → "Public Networking"

---

#### 🟦 **OPTION C: Vercel** (All-in-one, but Python support newer)

1. Go to [Vercel.com](https://vercel.com)
2. Click **"Add New"** → **"Project"**
3. Select your GitHub repository
4. **Root Directory**: `.` (current)
5. **Environment Variables**:
   - `GROQ_API_KEY` = [Your Groq API key]
6. **Deploy**
7. Get URL from Dashboard

---

### STEP 4: Deploy Frontend on Vercel (10 minutes)

1. Go to [Vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Select your repository
4. **Configuration**:
   - **Framework**: `Next.js` (auto-detected)
   - **Root Directory**: `frontend-nextjs`
   - **Build Command**: `npm run build` (auto-filled)
   - **Install Command**: `npm install` (auto-filled)
5. **Environment Variables** (CRITICAL):
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL from Step 3 (e.g., `https://zomato-ai-api.onrender.com`)
6. Click **"Deploy"**
7. Wait for build (3-5 minutes)
8. **Your frontend URL**: Shown in Vercel Dashboard

---

### STEP 5: Update Frontend Code (1 minute)

Your frontend already checks for the API URL, but verify it's correct.

**Check [frontend-nextjs/components/PreferenceForm.tsx](frontend-nextjs/components/PreferenceForm.tsx):**

```typescript
// Should use environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860';

// API calls should use:
axios.post(`${API_URL}/api/recommendations`, preferenceData)
```

If needed, update any hardcoded `localhost` URLs to use the environment variable.

---

### STEP 6: Test End-to-End (5 minutes)

1. **Open your frontend**: `https://your-frontend-url.vercel.app`
2. **Try the recommendation form**:
   - Select a city
   - Choose cuisine
   - Set budget and rating
   - Submit
3. **Check browser console** (F12) for errors
4. **If API request fails**:
   - Verify backend is running: Visit `/docs` endpoint
   - Check Network tab to see actual request/response
   - Confirm `NEXT_PUBLIC_API_URL` environment variable is set correctly

---

## 📋 Verification Checklist

### Before Deployment
- [ ] `git status` shows everything committed
- [ ] `.env` file is in `.gitignore` (NEVER commit secrets)
- [ ] `requirements.txt` has all Python dependencies
- [ ] `frontend-nextjs/package.json` has all Node dependencies
- [ ] Code works locally: `uvicorn run_phase5_api:app --reload` + `npm run dev` in frontend

### During Deployment
- [ ] GitHub repository created and code pushed
- [ ] Backend deployed (Render/Railway/Vercel)
- [ ] Backend `/docs` endpoint accessible
- [ ] Frontend deployed (Vercel)
- [ ] Environment variables set correctly

### After Deployment
- [ ] Frontend loads without errors
- [ ] Recommendation form submits successfully
- [ ] Backend receives and processes requests
- [ ] Results display on frontend
- [ ] No CORS errors in console
- [ ] No 404 or 503 errors

---

## 🔑 Environment Variables Reference

### Backend (Render/Railway/Vercel Dashboard)
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Frontend (Vercel Dashboard)
```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

**⚠️ IMPORTANT**: 
- `.env` files are LOCAL ONLY (never commit)
- Deployment platforms inject variables automatically
- `NEXT_PUBLIC_` prefix is required for frontend environment variables (it embeds in build)

---

## 🐛 Troubleshooting

### Backend Won't Deploy
**Error**: Build fails with missing dependencies
```bash
# Solution: Test locally first
pip install -r requirements.txt
uvicorn run_phase5_api:app --reload
```

**Error**: Port configuration issue
```bash
# The Dockerfile and deployment commands should use $PORT variable
# Render/Railway/Vercel automatically set this
```

### Frontend Can't Connect to Backend
**Error**: CORS error in console
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution**: CORS is already enabled in `run_phase5_api.py` with `allow_origins=["*"]`
- For production, restrict to your frontend domain
- Update in [run_phase5_api.py](run_phase5_api.py):
```python
allow_origins=["https://your-frontend-url.vercel.app"]
```

**Error**: API URL returns 404
```
Solution: Check NEXT_PUBLIC_API_URL in Vercel dashboard
- Should be: https://your-backend-domain.com (no trailing slash)
- NOT: http://localhost:7860
```

### Deployment Platform Issues
- **Render**: Check Logs tab for build/runtime errors
- **Railway**: See Deployments tab
- **Vercel**: Check Deployments tab or use `vercel logs`

---

## 📞 Getting Help

### If Backend Doesn't Start
1. Check deployment logs for Python errors
2. Verify `requirements.txt` is correct
3. Ensure `GROQ_API_KEY` is set in environment
4. Try running locally: `uvicorn run_phase5_api:app --reload`

### If Frontend Shows Blank Page
1. Check Vercel build logs
2. Open DevTools Console (F12) for JavaScript errors
3. Verify `NEXT_PUBLIC_API_URL` matches your backend domain
4. Try `npm run build` locally to replicate build environment

### If API Calls Fail
1. Check backend is running: Visit `https://your-backend-domain.com/docs`
2. Check frontend environment variable: Right-click → Inspect → Console
3. Look for CORS errors or 502/503 responses
4. Check backend logs in deployment platform

---

## 🎉 Success Indicators

Your deployment is successful when:
1. ✅ Frontend loads at Vercel URL
2. ✅ Backend API accessible at deployment URL
3. ✅ Recommendation form processes requests
4. ✅ Results display correctly on frontend
5. ✅ No errors in browser console
6. ✅ Code changes reflect within minutes of `git push`

---

## 📈 What's Next?

### Monitoring & Maintenance
- Monitor deployment logs regularly
- Set up error notifications (Render/Railway/Vercel provide dashboards)
- Keep dependencies updated
- Monitor API usage and performance

### Scaling
- Render/Railway can scale automatically
- Vercel handles frontend scaling automatically
- Add caching layer for frequently recommended restaurants
- Consider database for session management

### Security
- Restrict CORS to your domain only
- Keep API keys secure (use deployment platform secrets)
- Add rate limiting to API
- Implement request validation and sanitization

---

## 📞 Support

**For Deployment Platform Help:**
- Render: [docs.render.com](https://docs.render.com)
- Railway: [docs.railway.app](https://docs.railway.app)
- Vercel: [vercel.com/docs](https://vercel.com/docs)

**For Your Project:**
- Backend Issues: Check `run_phase5_api.py` and logs
- Frontend Issues: Check `frontend-nextjs/` and browser console
- API Issues: Visit deployment URL `/docs` for Swagger UI

---

**🚀 Your system is ready for production! Deploy confidently.**
