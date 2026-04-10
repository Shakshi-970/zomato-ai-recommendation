'use client';

interface RecommendationCardProps {
  restaurant: {
    restaurant_id: string;
    name: string;
    cuisine: string;
    locality: string;
    rating: number;
    estimated_cost: number;
    explanation?: string;
    source?: string;
  };
  index: number;
}

const RESTAURANT_IMAGES = [
  'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80',
  'https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=800&q=80',
  'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=800&q=80',
  'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80',
  'https://images.unsplash.com/photo-1481833761820-0509d3217039?w=800&q=80',
  'https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=800&q=80',
];

export default function RecommendationCard({ restaurant, index }: RecommendationCardProps) {
  const cuisinesArray = restaurant.cuisine.split(',').slice(0, 2).map((c) => c.trim());
  const imageUrl = RESTAURANT_IMAGES[index % RESTAURANT_IMAGES.length];

  return (
    <div className="bg-white rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:scale-105 border border-gray-100">
      <div className="relative w-full h-52 bg-gray-200 overflow-hidden">
        <img
          src={imageUrl}
          alt={restaurant.name}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/600x400?text=' + encodeURIComponent(restaurant.name);
          }}
        />
        <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-sm px-3 py-2 rounded-full text-sm font-semibold text-gray-900 shadow-lg border border-gray-200">
          <span className="flex items-center gap-1">
            ⭐ {restaurant.rating.toFixed(1)}
          </span>
        </div>
        {restaurant.source === 'llm' && (
          <div className="absolute top-4 right-4 bg-gradient-to-r from-red-500 to-red-700 px-3 py-1 rounded-full text-xs font-bold text-white shadow-lg">
            AI Ranked
          </div>
        )}
      </div>

      <div className="p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-2 leading-tight">{restaurant.name}</h3>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span>📍</span>
              <span>{restaurant.locality}</span>
            </div>
          </div>
          <div className="text-right">
            <p className="text-lg font-bold text-gray-900">₹{restaurant.estimated_cost.toLocaleString()}</p>
            <p className="text-xs text-gray-500">for two</p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {cuisinesArray.map((cuisine, idx) => (
            <span key={idx} className="rounded-full bg-red-50 px-3 py-1 text-xs font-medium text-red-700 border border-red-200">
              {cuisine}
            </span>
          ))}
        </div>

        {restaurant.explanation && (
          <div className="mb-4 rounded-2xl bg-gradient-to-br from-slate-50 to-gray-50 p-4 text-sm text-slate-700 border border-slate-200">
            <div className="flex items-start gap-2">
              <span className="text-lg">🤖</span>
              <div>
                <span className="font-semibold text-slate-900 block mb-1">AI Insights:</span>
                <span className="text-slate-700 leading-relaxed">{restaurant.explanation}</span>
              </div>
            </div>
          </div>
        )}

        <div className="flex gap-3">
          <button className="flex-1 rounded-2xl bg-gradient-to-r from-red-500 to-red-700 px-4 py-3 text-sm font-bold text-white shadow-lg transition-all transform hover:scale-105 hover:shadow-xl">
            View Menu
          </button>
          <button className="rounded-2xl bg-gray-100 px-4 py-3 text-sm font-semibold text-gray-700 transition-all hover:bg-gray-200 border border-gray-200">
            ❤️
          </button>
        </div>
      </div>
    </div>
  );
}
