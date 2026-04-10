# AI Restaurant Recommendation Frontend (Next.js)

A modern, responsive Next.js frontend for the AI-powered restaurant recommendation system, inspired by Zomato's design.

## Features

- **Modern UI Design**: Clean, professional interface with Tailwind CSS
- **Two-Column Layout**: Preference form on the left, recommendations on the right
- **Real-time Recommendations**: Integrates with the backend API on port 8080
- **Restaurant Cards**: Display restaurants with ratings, cost, location, and AI insights
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Loading States**: Beautiful loading spinner while generating recommendations
- **Error Handling**: Clear error messages for API failures

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Node.js**: 16+

## Setup & Installation

### Prerequisites
- Node.js 16 or higher
- npm or yarn package manager

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend-nextjs
```

2. Install dependencies:
```bash
npm install
```

3. Set environment variables (already configured in `.env.local`):
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8080
```

### Running the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend-nextjs/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Home page with main logic
│   └── globals.css         # Global styles and Tailwind imports
├── components/
│   ├── Header.tsx          # Top header with logo and search
│   ├── PreferenceForm.tsx  # Left panel: user preferences form
│   ├── RecommendationCard.tsx   # Individual restaurant card
│   ├── RecommendationsContainer.tsx  # Grid of recommendations
│   └── LoadingSpinner.tsx  # Loading animation
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
├── postcss.config.js
└── .env.local
```

## API Integration

The frontend communicates with the backend API (running on `http://127.0.0.1:8080`) with the following endpoint:

### POST `/phase5/recommend`

**Request:**
```json
{
  "locality": "Koramangala",
  "budget": 1000,
  "additional_details": "Optional user preference details"
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "restaurant_id": "123",
      "name": "Restaurant Name",
      "city": "Bengaluru",
      "locality": "Koramangala",
      "cuisines": "Italian, Continental",
      "rating": 4.4,
      "avg_cost_for_two": 1200,
      "votes": 850,
      "ai_insight": "Highly rated for wood-fired pizzas..."
    }
  ]
}
```

## Features & Components

### Header Component
- Logo and branding
- Location selector
- Search functionality
- User profile menu

### PreferenceForm Component
- 30 locality options dropdown
- Budget slider (₹200 - ₹3000)
- Optional cuisine preferences
- Additional details text area
- Submit button with loading state

### RecommendationCard Component
- Restaurant image
- Name and rating with vote count
- Location (locality)
- Cost for two
- Cuisine tags
- AI-generated insight
- View Menu button

### RecommendationsContainer Component
- Grid layout (responsive: 1-2-3 columns)
- Personalized greeting
- Empty state message

## Styling

### Colors
- Primary: Red (#EF4F5F) - accent color
- Dark: #1A1A1A - text
- Light: #F5F5F5 - backgrounds

### Responsive Breakpoints
- Mobile: < 768px (1 column)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (3 columns)

## Development Tips

1. **API Debugging**: Check the browser's Network tab in DevTools to see API requests
2. **Error Handling**: Errors are displayed in a red banner at the top of the page
3. **Loading State**: The submit button is disabled during API calls
4. **Image Fallback**: Uses placeholder images if restaurant images fail to load

## Known Issues & Future Improvements

- [ ] Add actual restaurant images from a CDN or image service
- [ ] Implement favorite/bookmark functionality
- [ ] Add filters for cuisine type, rating, cost range
- [ ] Add restaurant details page with full menu
- [ ] Implement user authentication and saved preferences
- [ ] Add pagination for large result sets
- [ ] Cache recommendations to reduce API calls
- [ ] Add animations and micro-interactions

## Troubleshooting

### "Failed to connect to API"
- Ensure the backend is running on `http://127.0.0.1:8080`
- Check the `.env.local` file for correct API_URL
- Check browser console for CORS errors

### Port already in use
```bash
# Kill process using port 3000
kill -9 $(lsof -t -i :3000)
```

### Dependency issues
```bash
rm -rf node_modules package-lock.json
npm install
```

## License

Part of the AI Restaurant Recommendation System project.
