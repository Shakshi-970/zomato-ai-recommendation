# Deploy Both Backend & Frontend on Vercel (Free)

## Overview

Vercel now supports Python serverless functions! You can deploy both your Next.js frontend and FastAPI backend entirely on Vercel for free.

---

## Architecture

```
Vercel (Single Platform)
├── Frontend: /frontend-nextjs (Next.js)
│   └── Deployed as Static Site + Edge Functions
└── Backend: /api/index.py (FastAPI Serverless)
    └── Deployed as Serverless Functions
```

**Result**: `https://your-project.vercel.app` hosts both!

---

## Step 1: Create Vercel API Handler

### Create the directory structure:
```
zomato-ai-recommendation/
├── api/
│   └── index.py          ← NEW: FastAPI handler for Vercel
├── frontend-nextjs/
├── src/
├── data/
└── ... (existing files)
```

### Create `/api/index.py`:

This file exports your FastAPI app as a Vercel serverless function.

```python
# /api/index.py
"""
Vercel Serverless FastAPI Handler
This makes the FastAPI app compatible with Vercel's serverless functions.
"""

import sys
from pathlib import Path

# Add project root to Python path so imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import your existing FastAPI app
from run_phase5_api import app

# Vercel requires the app to be exported as 'app'
# No changes needed - just re-export it
__all__ = ["app"]
```

---

## Step 2: Create `vercel.json` Configuration

Create a `vercel.json` file in your project root:

```json
{
  "buildCommand": "pip install -r requirements.txt && cd frontend-nextjs && npm install && npm run build",
  "outputDirectory": "frontend-nextjs/.next",
  "framework": "nextjs",
  "env": {
    "GROQ_API_KEY": "@groq_api_key",
    "NEXT_PUBLIC_API_URL": "@api_url"
  },
  "functions": {
    "api/index.py": {
      "memory": 1024,
      "maxDuration": 60,
      "runtime": "python3.11"
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend-nextjs/$1"
    }
  ]
}
```

---

## Step 3: Update Environment Variables

### Create `.env.local` for local testing:
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### For Vercel Dashboard:
Set these environment variables:

```
GROQ_API_KEY = (your Groq API key from https://console.groq.com/keys)
NEXT_PUBLIC_API_URL = https://your-project.vercel.app
```

---

## Step 4: Update Frontend API Base URL

Edit `frontend-nextjs/components/PreferenceForm.tsx` to use the environment variable:

```typescript
// At the top of the component
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';

// In your API calls, use the same domain:
const response = await axios.post(`${API_BASE}/api/recommendations`, preferenceData);
```

---

## Step 5: Push to GitHub and Deploy

```bash
# Stage changes
git add .

# Commit
git commit -m "Configure for Vercel: Add serverless API handler and Vercel config"

# Push
git push origin main
```

---

## Step 6: Deploy on Vercel

### Option A: Using Vercel CLI

```bash
# Install Vercel CLI (if not already installed)
npm install -g vercel

# Deploy
cd "c:\Users\shakshi.d.singh\OneDrive - Accenture\zomato ai recommendation"
vercel --prod

# Follow prompts and set environment variables
```

### Option B: Using Vercel Dashboard

1. Go to [Vercel.com](https://vercel.com)
2. Click **"Add New"** → **"Project"**
3. Select your GitHub repository
4. **Root Directory**: `.` (current)
5. **Framework**: Detect automatically
6. **Build Command**: Leave as auto-detected OR use:
   ```
   pip install -r requirements.txt && cd frontend-nextjs && npm install && npm run build
   ```
7. **Environment Variables**:
   ```
   GROQ_API_KEY = (your key)
   NEXT_PUBLIC_API_URL = https://your-project.vercel.app
   ```
8. Click **"Deploy"**

---

## Step 7: Test Everything

### Test Backend API
```
Visit: https://your-project.vercel.app/api/docs
```
You should see Swagger API documentation.

### Test Frontend
```
Visit: https://your-project.vercel.app
```
You should see your recommendation form.

### Test End-to-End
1. Fill the preference form
2. Submit
3. See recommendations appear
4. Open DevTools (F12) → Network tab → No CORS errors

---

## Complete File Structure After Setup

```
zomato-ai-recommendation/
├── api/
│   └── index.py                    ← NEW
├── frontend-nextjs/
│   ├── app/
│   ├── components/
│   ├── package.json
│   └── ... (existing)
├── src/
│   ├── phase5/
│   ├── auth/
│   └── ... (existing)
├── data/
│   └── processed/
│       └── restaurants_clean.csv
├── vercel.json                     ← NEW
├── run_phase5_api.py               ← EXISTING
├── requirements.txt                ← EXISTING
├── .env                            ← LOCAL ONLY
├── .gitignore                      ← EXISTING
└── ... (other files)
```

---

## Differences from Render Deployment

| Aspect | Render | Vercel |
|--------|--------|--------|
| **Cost** | Free tier → Paid | Always free |
| **Setup** | Web service | Serverless functions |
| **Cold starts** | ~5-10 sec | ~1-2 sec |
| **Scaling** | Manual/Auto | Automatic |
| **Both on one platform** | ❌ No | ✅ Yes |
| **Deployment** | Docker | Git push |

---

## Troubleshooting

### "Python module not found"
Make sure `requirements.txt` includes all dependencies:
```
fastapi
uvicorn[standard]
pandas
pyarrow
groq
python-dotenv
pydantic
```

### "API returns 404"
Ensure your API calls use: `https://your-project.vercel.app/api/...`
NOT: `https://your-project.vercel.app/docs` (that's frontend routing)

### "Frontend can't reach backend"
1. Check `NEXT_PUBLIC_API_URL` is set in Vercel dashboard
2. Verify it equals your Vercel domain
3. Check browser console for actual error messages

### "Build fails"
Check Vercel build logs:
1. Go to Vercel Dashboard
2. Select your project
3. Click **"Deployments"**
4. Click failed deployment
5. View **"Build Logs"**

---

## Quick Deployment Checklist

- [ ] Created `/api/index.py` with FastAPI handler
- [ ] Created `vercel.json` configuration
- [ ] Updated `NEXT_PUBLIC_API_URL` in frontend components
- [ ] Added files to Git and pushed to GitHub
- [ ] Set `GROQ_API_KEY` in Vercel dashboard
- [ ] Set `NEXT_PUBLIC_API_URL` in Vercel dashboard
- [ ] Frontend loads at `https://your-project.vercel.app`
- [ ] Backend API accessible at `/api/docs`
- [ ] End-to-end test successful

---

## Your Vercel URLs

```
Frontend & Backend: https://zomato-ai-recommendation.vercel.app
API Documentation: https://zomato-ai-recommendation.vercel.app/api/docs
Health Check: https://zomato-ai-recommendation.vercel.app/api/phase5/health
```

---

## Next Steps

1. ✅ Create `/api/index.py`
2. ✅ Create `vercel.json`
3. ✅ Push to GitHub
4. ✅ Deploy on Vercel
5. ✅ Test everything
6. ✅ Share your deployed app!

**Both backend and frontend on one Vercel domain = simpler, cheaper, and just as powerful! 🚀**
