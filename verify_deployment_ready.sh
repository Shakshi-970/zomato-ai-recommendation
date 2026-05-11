#!/bin/bash
# Production Deployment Verification Script
# Run this before pushing to GitHub and deploying

echo "🔍 Checking Project Setup for Deployment..."
echo ""

# Check 1: Git initialized
echo "✓ Git Status:"
if [ -d .git ]; then
    echo "  ✅ Git repository found"
    git log --oneline -n 1 || echo "  ⚠️  No commits yet"
else
    echo "  ❌ Git not initialized. Run: git init"
fi
echo ""

# Check 2: .gitignore present
echo "✓ .gitignore Configuration:"
if [ -f .gitignore ]; then
    echo "  ✅ .gitignore exists"
    if grep -q ".env" .gitignore; then
        echo "  ✅ .env properly ignored"
    else
        echo "  ⚠️  .env not in .gitignore - SECRETS WILL BE EXPOSED!"
    fi
else
    echo "  ❌ .gitignore missing"
fi
echo ""

# Check 3: Backend requirements
echo "✓ Backend Dependencies (requirements.txt):"
if [ -f requirements.txt ]; then
    echo "  ✅ requirements.txt found"
    echo "  Packages:"
    head -n 10 requirements.txt | sed 's/^/    - /'
else
    echo "  ❌ requirements.txt missing"
fi
echo ""

# Check 4: Frontend package.json
echo "✓ Frontend Dependencies (package.json):"
if [ -f frontend-nextjs/package.json ]; then
    echo "  ✅ frontend-nextjs/package.json found"
else
    echo "  ❌ frontend-nextjs/package.json missing"
fi
echo ""

# Check 5: API Configuration
echo "✓ API Configuration:"
if [ -f run_phase5_api.py ]; then
    echo "  ✅ run_phase5_api.py found"
    if grep -q "CORSMiddleware" run_phase5_api.py; then
        echo "  ✅ CORS middleware configured"
    else
        echo "  ⚠️  CORS might not be configured"
    fi
else
    echo "  ❌ run_phase5_api.py missing"
fi
echo ""

# Check 6: Dockerfile
echo "✓ Docker Configuration:"
if [ -f Dockerfile ]; then
    echo "  ✅ Dockerfile found"
else
    echo "  ❌ Dockerfile missing (needed for some platforms)"
fi
echo ""

# Check 7: Environment variables
echo "✓ Environment Variables:"
if [ -f .env ]; then
    echo "  ⚠️  .env file found locally"
    echo "  📌 REMEMBER: This should NOT be committed (check .gitignore)"
else
    echo "  ℹ️  .env file not found (create it locally with GROQ_API_KEY)"
fi
echo ""

# Check 8: Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 DEPLOYMENT CHECKLIST:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Before pushing to GitHub:"
echo "  [ ] All code is committed: git add . && git commit -m 'message'"
echo "  [ ] .env is NOT in Git (check: git status)"
echo "  [ ] requirements.txt has all packages"
echo "  [ ] API port can be configured via PORT env var"
echo ""
echo "Before deploying to Vercel/Render:"
echo "  [ ] Create GitHub repository"
echo "  [ ] Push code: git push -u origin main"
echo "  [ ] Connect platform to GitHub"
echo "  [ ] Set GROQ_API_KEY environment variable in platform"
echo "  [ ] (Frontend) Set NEXT_PUBLIC_API_URL to backend URL"
echo ""
echo "✅ Run this verification regularly before deployments!"
echo ""
