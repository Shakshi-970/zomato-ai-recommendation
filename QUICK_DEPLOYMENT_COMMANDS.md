# Quick Git & Deployment Commands

## ⚡ Copy-Paste Commands for GitHub Push

```bash
# 1. Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Check current status
git status

# 3. Stage all changes
git add .

# 4. Commit
git commit -m "Initial commit: Zomato AI recommendation system with Phase 5 API, Next.js frontend, and authentication"

# 5. Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/zomato-ai-recommendation.git

# 6. Push to GitHub
git branch -M main
git push -u origin main

# 7. Verify it worked
git remote -v
```

---

## 📋 Deployment Commands

### For Backend Deployment

**Option 1: Render** (Recommended)
```bash
# Just connect GitHub in Render dashboard
# Set environment variable in Render:
# GROQ_API_KEY=your_groq_api_key

# Build Command: pip install -r requirements.txt
# Start Command: uvicorn run_phase5_api:app --host 0.0.0.0 --port $PORT
```

**Option 2: Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

---

### For Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
cd frontend-nextjs
vercel --prod

# Then set environment variable in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend-url
```

---

## 🔑 Required Secrets

### Render/Railway Backend
```
GROQ_API_KEY = (your Groq API key)
```

### Vercel Frontend
```
NEXT_PUBLIC_API_URL = (your backend URL, e.g., https://zomato-ai-api.onrender.com)
```

---

## 🧪 Local Testing Before Deployment

```bash
# Test backend locally
pip install -r requirements.txt
uvicorn run_phase5_api:app --reload
# Visit: http://localhost:8000/docs

# Test frontend locally (in different terminal)
cd frontend-nextjs
npm install
npm run dev
# Visit: http://localhost:3000
```

---

## ✅ Verification Checklist

- [ ] Code pushed to GitHub: `git remote -v` shows origin
- [ ] Backend API running: Visit `/docs` endpoint
- [ ] Frontend loads without errors
- [ ] API calls working: Check Network tab in DevTools
- [ ] Environment variables set in deployment platforms
- [ ] CORS working (no 403 errors in console)

---

## 🚨 If Something Goes Wrong

```bash
# Check Git log
git log --oneline -n 10

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (lose changes)
git reset --hard HEAD~1

# Check what's being ignored
cat .gitignore

# Force add a file if needed
git add -f filename.txt
```

---

## 📌 URLs After Deployment

- **Frontend**: `https://your-project-name.vercel.app`
- **Backend**: `https://your-project-name.onrender.com`
- **Backend Docs**: `https://your-project-name.onrender.com/docs`

---

**Once all steps are complete, your app will be live! 🚀**
