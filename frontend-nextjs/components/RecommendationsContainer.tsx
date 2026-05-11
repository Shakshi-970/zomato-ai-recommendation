'use client';

import RecommendationCard from './RecommendationCard';
import LoadingSpinner from './LoadingSpinner';

interface Restaurant {
  restaurant_id: string;
  name: string;
  cuisine: string;
  locality: string;
  rating: number;
  estimated_cost: number;
  explanation?: string;
  source?: string;
}

const PLACEHOLDER_RECOMMENDATIONS: Restaurant[] = [
  {
    restaurant_id: 'placeholder-1',
    name: 'The Pizza Bakery',
    cuisine: 'Italian, Cafe',
    locality: 'Koramangala 5th Block',
    rating: 4.6,
    estimated_cost: 1800,
    explanation: 'Highly rated for wood-fired pizzas, outdoor patio, and craft beers. Perfect for a casual evening.',
    source: 'Sample',
  },
  {
    restaurant_id: 'placeholder-2',
    name: 'Bistro Claytopia',
    cuisine: 'Italian, Cafe',
    locality: 'Koramangala 1st Block',
    rating: 4.4,
    estimated_cost: 1200,
    explanation: 'Charming cafe known for its artsy vibe, garden seating, and delicious Italian small plates.',
    source: 'Sample',
  },
  {
    restaurant_id: 'placeholder-3',
    name: 'Chianti',
    cuisine: 'Italian, Fine Dining',
    locality: 'Koramangala 5th Block',
    rating: 4.5,
    estimated_cost: 2200,
    explanation: 'Authentic Italian restaurant, recommended for its romantic ambiance, extensive wine list, and pasta dishes.',
    source: 'Sample',
  },
];

interface RecommendationsContainerProps {
  recommendations: Restaurant[];
  isLoading: boolean;
  userPreference?: string;
  userName?: string;
}

export default function RecommendationsContainer({
  recommendations,
  isLoading,
  userPreference = '',
  userName = '',
}: RecommendationsContainerProps) {
  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (recommendations.length === 0) {
    return (
      <div>
        <div className="rounded-3xl bg-white p-8 shadow-xl mb-6 border border-gray-100">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-red-700 rounded-2xl flex items-center justify-center">
              <span className="text-white text-2xl">🤖</span>
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Personalized AI Recommendations</h2>
              <p className="text-gray-700 text-base leading-relaxed">
                👉 Hi {userName ? userName : 'there'}! Set your preferences on the left and click "Generate Recommendations" to discover restaurants!
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {PLACEHOLDER_RECOMMENDATIONS.map((restaurant, index) => (
            <RecommendationCard key={restaurant.restaurant_id} restaurant={restaurant} index={index} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 rounded-3xl bg-white p-8 shadow-xl border border-gray-100">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-red-700 rounded-2xl flex items-center justify-center">
            <span className="text-white text-2xl">🤖</span>
          </div>
          <div className="flex-1">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Personalized AI Recommendations</h2>
            <p className="text-gray-700 text-base leading-relaxed">
              {userPreference ||
                'Hi there! Set your preferences on the left and AI will suggest the best restaurants for you.'}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations.map((restaurant, index) => (
          <RecommendationCard
            key={restaurant.restaurant_id}
            restaurant={restaurant}
            index={index}
          />
        ))}
      </div>
    </div>
  );
}
