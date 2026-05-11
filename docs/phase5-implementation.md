# Phase 5 Implementation Guide

## What is implemented
- **End-to-End Orchestration Service**: Coordinates Phases 2-4 for complete recommendation workflow
- **FastAPI Endpoints**: Single `/phase5/recommend` endpoint that orchestrates all phases
- **Beautiful Frontend UI**: HTML/CSS/JavaScript interface for testing and user interaction
- **Complete E2E Testing**: Full workflow from user input to final recommendations

## Core Components

### 1. End-to-End Orchestrator (`src/phase5/service.py`)
- Coordinates all phases: preference validation → candidate retrieval → LLM ranking
- Handles error cases gracefully
- Provides detailed workflow status in response
- Integrates Phase 2, 3, and 4 services

### 2. API Endpoints (`src/phase5/api.py`)
- `POST /phase5/recommend` - Main recommendation endpoint
- `GET /phase5/health` - Health check
- Full request/response validation with Pydantic
- CORS enabled for frontend access

### 3. Frontend UI (`index.html`)
- **Input Form**:
  - City/location selection
  - Budget tier or custom amount
  - Cuisine preferences (checkboxes)
  - Minimum rating
  - Number of recommendations
  
- **Results Display**:
  - Phase status visualization (validation → retrieval → ranking)
  - Summary from LLM
  - Ranked recommendation cards with details
  - Metadata and cost tracking

## API Details

### Endpoint: `POST /phase5/recommend`

**Request:**
```json
{
  "location": "Bangalore",
  "budget_tier": "medium",
  "budget": 1500,
  "preferred_cuisines": ["Italian", "Chinese"],
  "min_rating": 3.5,
  "additional_preferences": [],
  "top_k": 5
}
```

**Response:**
```json
{
  "query_id": "e2e_1775489763_17b520d7",
  "preference_valid": true,
  "preference_errors": [],
  "normalized_preference": {
    "location": "Bangalore",
    "budget_tier": "medium",
    "preferred_cuisines": ["Chinese", "Italian"],
    "min_rating": 3.5,
    "additional_preferences": [],
    "top_k": 5
  },
  "total_candidates": 150,
  "selected_candidates": 50,
  "recommendations": [
    {
      "rank": 1,
      "name": "Bella Italia",
      "cuisine": "Italian, Pizza",
      "rating": 4.4,
      "estimated_cost": 1200,
      "explanation": "Bella Italia perfectly matches...",
      "source": "llm"
    }
  ],
  "summary": "Based on your preferences, the top picks are...",
  "tokens_used": 1025,
  "cost_usd": 0.0512
}
```

## Architecture Flow

```
User Input (HTML Form)
    ↓
[Phase 5 API: /phase5/recommend]
    ↓
    ├─→ Phase 2: Preference Validation
    │   └─→ Normalize location, budget, cuisines
    │
    ├─→ Phase 3: Candidate Retrieval
    │   └─→ Filter and score restaurants
    │
    ├─→ Phase 4: LLM Ranking
    │   └─→ Generate rankings and explanations
    │
    └─→ Response Formatting
        └─→ Return complete result with metadata
        
Frontend Display
    ↓
User Views Recommendations
```

## Run Instructions

### Step 1: Start All Required Services

**Terminal 1 - Phase 5 API (End-to-End Orchestrator)**
```bash
python run_phase5_api.py
```
Server: http://127.0.0.1:8003

### Step 2: Open Frontend

Open in browser:
```
file:///c:/Users/shakshi.d.singh/OneDrive - Accenture/M1/index.html
```

Or simply double-click `index.html` to open in default browser.

## Features

### User Experience
- **Intuitive Form**: Easy preference input with presets for common cuisines
- **Real-time Status**: Visual feedback showing each phase completion
- **Detailed Results**: Recommendations with ratings, costs, and AI explanations
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading Indicator**: Visual spinner during API processing

### Technical Features
- **Full Type Safety**: Pydantic validation throughout
- **Error Handling**: Graceful error messages for invalid inputs
- **Cost Tracking**: Shows USD cost per recommendation
- **Query Tracking**: Unique ID for each request
- **CORS Enabled**: Frontend can call API from different origins

## Exit Criteria (Achieved ✅)

### End-to-End Testing
- ✅ Form accepts user preferences
- ✅ Preferences validated (Phase 2)
- ✅ Candidates retrieved and scored (Phase 3)
- ✅ LLM ranking applied (Phase 4)
- ✅ Results displayed beautifully

### Response Time
- ✅ < 5 seconds total E2E latency
- ✅ Phase status updates visible
- ✅ Non-blocking UI during processing

### Functionality
- ✅ Multiple cuisine selection
- ✅ Budget tier and custom amount support
- ✅ Rating preference handling
- ✅ Flexible recommendation count (3-10)
- ✅ Error handling for invalid locations

## Testing End-to-End

### Test Case 1: Italian, Medium Budget, Bangalore
1. Open index.html
2. Enter Location: "Bangalore"
3. Select Budget Tier: "medium"
4. Check Cuisines: "Italian", "Pizza"
5. Set Min Rating: 3.5
6. Click "Get Recommendations"
7. Expected: 3-5 Italian restaurants with ratings and explanations

### Test Case 2: Chinese, Low Budget, Mumbai
1. Enter Location: "Mumbai"
2. Select Budget Tier: "low"
3. Check Cuisines: "Chinese", "Asian"
4. Set Min Rating: 3.0
5. Top K: 5
6. Expected: 5 budget-friendly restaurants

### Test Case 3: North Indian, High Budget, Delhi
1. Enter Location: "Delhi"
2. Select Budget Tier: "high"
3. Check Cuisines: "North Indian", "Biryani"
4. Set Min Rating: 4.0
5. Expected: Premium restaurants with high ratings

## Troubleshooting

### "Failed to get recommendations" error
- Make sure the Phase 5 API server is running on port 8003
- Check that all previous phases (Phase 2, 3, 4) are working
- Check browser console for CORS or network errors

### No candidates found
- Try different cuisine selections
- Lower the minimum rating requirement
- Check that the city is spelled correctly

### Slow responses
- This is normal for the first request (LLM warm-up)
- Subsequent requests should be faster
- Check system resources

## Files

- `src/phase5/__init__.py` - Module init
- `src/phase5/service.py` - Orchestration service
- `src/phase5/api.py` - FastAPI endpoints
- `run_phase5_api.py` - API server launcher
- `index.html` - Frontend UI

## Architecture Integration

This Phase 5 UI ties together all previous phases:
- **Phase 2**: Normalizes user preferences
- **Phase 3**: Retrieves relevant candidate restaurants
- **Phase 4**: Uses LLM to rank and explain recommendations
- **Phase 5**: Orchestrates and presents to user

## Future Enhancements

1. **Backend Database**: Store preferences and feedback
2. **User Accounts**: Save favorite restaurants
3. **Map Integration**: Show restaurant locations
4. **Direct Links**: Links to restaurant pages
5. **Rating System**: User feedback on recommendations
6. **Export**: Save recommendations as PDF/image
7. **Mobile App**: Native mobile application
8. **Restaurant Details**: Full menu, photos, hours, reviews
