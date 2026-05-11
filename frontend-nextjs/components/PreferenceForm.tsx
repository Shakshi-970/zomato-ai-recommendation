'use client';

import { FormEvent, useEffect, useState } from 'react';
import SearchableDropdown from './SearchableDropdown';

const CUISINES = ['Italian', 'North Indian', 'Chinese', 'Cafe', 'Street Food', 'South Indian', 'Continental'];
const DINING_TYPES = ['Delivery', 'Dine-in', 'Date Night', 'Casual'];

function StarRating({ value, onChange }: { value: number; onChange: (val: number) => void }) {
  const [hovered, setHovered] = useState(0);
  return (
    <div className="flex items-center gap-2 py-2">
      {[1, 2, 3, 4].map((star) => {
        const filled = star <= (hovered || value);
        return (
          <button
            key={star}
            type="button"
            onClick={() => onChange(value === star ? 0 : star)}
            onMouseEnter={() => setHovered(star)}
            onMouseLeave={() => setHovered(0)}
            className="focus:outline-none transition-transform hover:scale-110"
            aria-label={`${star} star${star > 1 ? 's' : ''}`}
          >
            <svg
              className={`w-9 h-9 transition-colors duration-150 ${filled ? 'text-yellow-400 drop-shadow-sm' : 'text-gray-300'}`}
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
            </svg>
          </button>
        );
      })}
      {value > 0 && (
        <span className="ml-1 text-sm font-semibold text-gray-700">{value}/4</span>
      )}
    </div>
  );
}

interface PreferenceFormProps {
  onSubmit: (preferences: any) => void;
  isLoading?: boolean;
  city: string;
  cities: string[];
  localities: string[];
  setCity: (city: string) => void;
}

export default function PreferenceForm({ onSubmit, isLoading = false, city, cities, localities, setCity }: PreferenceFormProps) {
  const [locality, setLocality] = useState(localities[0] || '');
  const [budget, setBudget] = useState<string>('');
  const [rating, setRating] = useState('');
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>(['Italian', 'North Indian', 'Cafe']);
  const [selectedDiningType, setSelectedDiningType] = useState<string>('Casual');
  const [additionalDetails, setAdditionalDetails] = useState('Find a cozy place with outdoor seating and a great view...');

  useEffect(() => {
    setLocality(localities[0] || '');
  }, [localities]);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const minRating = rating.trim() === '' ? 0 : Number(rating);
    const budgetAmount = budget.trim() === '' ? null : Number(budget);
    onSubmit({
      city,
      locality,
      budget: budgetAmount,
      rating: Number.isNaN(minRating) ? 0 : minRating,
      selectedCuisines,
      selectedDiningType,
      additionalDetails,
    });
  };

  const toggleCuisine = (cuisine: string) => {
    setSelectedCuisines((prev) =>
      prev.includes(cuisine)
        ? prev.filter((c) => c !== cuisine)
        : [...prev, cuisine]
    );
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl p-6 lg:p-8 sticky top-[100px] border border-gray-100">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-red-700 rounded-xl flex items-center justify-center">
          <span className="text-white text-xl">🍽️</span>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Set Your Preferences</h2>
          <p className="text-sm text-gray-500">Tell us what you're looking for</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <span>🏙️</span> City
          </label>
          <SearchableDropdown
            options={cities}
            value={city}
            onChange={setCity}
            placeholder="Select city"
            icon="🏙️"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <span>📍</span> Locality
          </label>
          <SearchableDropdown
            options={localities}
            value={locality}
            onChange={setLocality}
            placeholder="Select locality"
            icon="📍"
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-semibold text-gray-900 flex items-center gap-2">
              <span>🍜</span> Cuisine
            </label>
            <span className="text-sm text-gray-500">Choose up to 4</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {CUISINES.map((cuisine) => (
              <button
                key={cuisine}
                type="button"
                onClick={() => toggleCuisine(cuisine)}
                className={`rounded-full px-4 py-2 text-sm font-medium transition-all transform hover:scale-105 ${
                  selectedCuisines.includes(cuisine)
                    ? 'bg-gradient-to-r from-red-500 to-red-700 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border border-gray-200'
                }`}
              >
                {cuisine}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <span>💰</span> Budget
          </label>
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">₹</span>
            <input
              type="number"
              min={1}
              step={1}
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="w-full rounded-2xl border border-gray-200 bg-gray-50 pl-8 pr-4 py-3 text-gray-900 shadow-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-100 transition-all"
              placeholder="Enter budget"
            />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-semibold text-gray-900 flex items-center gap-2">
              <span>⭐</span> Minimum Rating
            </label>
            <span className="rounded-full bg-red-50 px-3 py-1 text-xs text-red-700">Optional</span>
          </div>
          <StarRating value={rating ? Number(rating) : 0} onChange={(val: number) => setRating(val === 0 ? '' : String(val))} />
          <p className="mt-2 text-xs text-gray-500">
            {rating ? `Showing restaurants rated ${rating}–${Number(rating) < 4 ? Number(rating) + 1 : '4+'}` : 'Click a star or leave blank for all ratings.'}
          </p>
        </div>

        <div>
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-semibold text-gray-900 flex items-center gap-2">
              <span>🍽️</span> Dining Type
            </label>
            <span className="text-sm text-gray-500">Pick one</span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {DINING_TYPES.map((type) => (
              <button
                key={type}
                type="button"
                onClick={() => setSelectedDiningType(selectedDiningType === type ? '' : type)}
                className={`rounded-2xl px-4 py-3 text-sm font-medium transition-all transform hover:scale-105 ${
                  selectedDiningType === type 
                    ? 'bg-gradient-to-r from-red-500 to-red-700 text-white shadow-lg' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border border-gray-200'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <span>💬</span> Add more details (Optional)
          </label>
          <textarea
            value={additionalDetails}
            onChange={(e) => setAdditionalDetails(e.target.value)}
            placeholder="Find a cozy place with outdoor seating and a great view..."
            className="w-full rounded-3xl border border-gray-200 bg-gray-50 px-4 py-4 text-sm text-gray-900 shadow-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-100 resize-none transition-all"
            rows={4}
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full rounded-3xl bg-gradient-to-r from-red-500 to-red-700 px-5 py-4 text-center text-sm font-bold uppercase tracking-wide text-white shadow-lg transition-all transform hover:scale-105 hover:shadow-xl disabled:cursor-not-allowed disabled:opacity-60 disabled:transform-none"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Generating...
            </span>
          ) : (
            '🚀 Generate Recommendations'
          )}
        </button>
      </form>
    </div>
  );
}
