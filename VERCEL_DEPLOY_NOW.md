# 🚀 Deploy Both Backend & Frontend on Vercel (Free & Easy)

## Why Vercel?
- ✅ **100% Free** - No subscription needed
- ✅ **One Platform** - Backend + Frontend together
- ✅ **Auto Scaling** - Handles traffic automatically
- ✅ **Git Connected** - Auto-deploy on every push
- ✅ **Serverless Python** - Your FastAPI runs as serverless functions

---

## What's Already Set Up ✓

Your project already has:
- ✅ `/api/index.py` - FastAPI handler for Vercel
- ✅ `vercel.json` - Deployment configuration  
- ✅ `frontend-nextjs/` - Next.js frontend ready
- ✅ Environment variables support

---

## 3 Steps to Deploy

### Step 1: Push to GitHub (You Already Did This ✓)

Your code is already on GitHub at:
```
https://github.com/Shakshi-970/zomato-ai-recommendation
```

### Step 2: Deploy on Vercel

**Go to [Vercel.com](https://vercel.com)**

1. Click **"Add New"** → **"Project"**
2. **Select Repository**: Click your `zomato-ai-recommendation` repo
3. **Configure**:
   - Root Directory: `.` (default)
   - Framework: Auto-detects Next.js ✓
   - Build Command: (Keep default)
4. Click **"Deploy"**
5. Wait 2-3 minutes for build ⏳

### Step 3: Set Environment Variables

**After deployment completes:**

1. Go to your project on Vercel Dashboard
2. Click **"Settings"** → **"Environment Variables"**
3. Add these variables:

```
GROQ_API_KEY = (your API key from https://console.groq.com/keys)
NEXT_PUBLIC_API_URL = https://your-project.vercel.app
```

4. Redeploy: Go to **"Deployments"** → Click **"..."** → **"Redeploy"**

---

## ✅ Verification

### After Deployment, Test:

1. **Frontend Loads**
   ```
   Visit: https://your-project.vercel.app
   You should see the recommendation form
   ```

2. **Backend API Works**
   ```
   Visit: https://your-project.vercel.app/api/docs
   You should see Swagger UI with all endpoints
   ```

3. **End-to-End Works**
   - Fill the form
   - Submit
   - See recommendations appear
   - No errors in browser console (F12)

---

## 📋 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] `GROQ_API_KEY` set in Vercel dashboard
- [ ] `NEXT_PUBLIC_API_URL` set to your Vercel domain
- [ ] Deployment completed successfully
- [ ] Frontend loads
- [ ] API endpoints accessible
- [ ] Recommendations working end-to-end

---

## Your Final URLs

```
🌐 Frontend: https://your-project.vercel.app
📚 API Docs: https://your-project.vercel.app/api/docs
🏥 Health:   https://your-project.vercel.app/api/phase5/health
```

---

## If You Get Errors

### "Build failed - Python error"
- Check Vercel logs: Deployments → Click failed → Build Logs
- Usually missing dependency in `requirements.txt`
- Fix and push again: `git push origin main` (auto-redeploys)

### "API returns 404"
- Verify `NEXT_PUBLIC_API_URL` in Vercel dashboard
- Should be exactly: `https://your-project.vercel.app` (no trailing slash)

### "Frontend can't reach backend"
- Check Network tab in browser DevTools (F12)
- Should see successful requests to `/api/...`
- If 503: Backend is sleeping, wait 30 seconds and retry

---

## 🎉 That's It!

Your complete system is live on **one Vercel domain** for **completely free**!

**Next time you want to deploy:**
```bash
git add .
git commit -m "Your changes"
git push origin main
# ← Vercel auto-deploys! No manual steps needed
```

---

## Useful Commands

```bash
# Check deployment status
git log --oneline -n 5

# View Vercel logs locally
npm install -g vercel
vercel logs https://your-project.vercel.app

# Redeploy without changes (if needed)
# Go to Vercel Dashboard → Deployments → Click "..." → Redeploy
```

---

**Your AI-powered restaurant recommendation system is now LIVE! 🚀🎉**
