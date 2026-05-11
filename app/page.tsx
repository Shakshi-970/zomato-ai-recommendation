'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import PreferenceForm from '@/components/PreferenceForm';
import RecommendationsContainer from '@/components/RecommendationsContainer';
import { useAuth } from '@/context/AuthContext';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8080';

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

interface LocationResponse {
  cities: string[];
  localities: string[];
}

function getBudgetTier(amount: number | null) {
  if (!amount) return null;
  if (amount <= 800) return 'low';
  if (amount <= 1800) return 'medium';
  return 'high';
}

export default function Home() {
  const { user, isLoaded, logout } = useAuth();
  const router = useRouter();

  const [availableCities, setAvailableCities] = useState<string[]>([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [localities, setLocalities] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<Restaurant[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userPreference, setUserPreference] = useState('');

  // Redirect to login if not authenticated
  useEffect(() => {
    if (isLoaded && !user) {
      router.push('/login');
    }
  }, [isLoaded, user, router]);

  useEffect(() => {
    const loadLocations = async () => {
      try {
        const response = await axios.get<LocationResponse>(`${API_BASE_URL}/phase5/locations`);
        const cities = response.data.cities;
        setAvailableCities(cities);
        if (cities.length) {
          setSelectedCity(cities[0]);
          setLocalities(response.data.localities || []);
        }
      } catch (err) {
        console.error('Failed to load locations:', err);
      }
    };
    loadLocations();
  }, []);

  useEffect(() => {
    if (!selectedCity) return;
    const loadLocalities = async () => {
      try {
        const response = await axios.get<LocationResponse>(`${API_BASE_URL}/phase5/locations`, {
          params: { city: selectedCity },
        });
        setLocalities(response.data.localities || []);
      } catch (err) {
        console.error('Failed to load localities:', err);
      }
    };
    loadLocalities();
  }, [selectedCity]);

  const handleSubmit = async (preferences: any) => {
    setIsLoading(true);
    setError(null);
    const localityValue = preferences.locality || localities[0] || '';

    try {
      const response = await axios.post(`${API_BASE_URL}/phase5/recommend`, {
        city: preferences.city,
        locality: localityValue,
        budget_tier: getBudgetTier(preferences.budget),
        budget: preferences.budget ?? null,
        preferred_cuisines: preferences.selectedCuisines,
        min_rating: preferences.rating,
        additional_preferences: preferences.additionalDetails ? [preferences.additionalDetails] : [],
        top_k: 6,
      });

      if (response.data.recommendations?.length > 0) {
        const transformed = response.data.recommendations.map((r: any, index: number) => ({
          restaurant_id: `${r.name}-${index}`,
          name: r.name,
          cuisine: r.cuisine,
          locality: preferences.locality,
          rating: r.rating,
          estimated_cost: r.estimated_cost,
          explanation: r.explanation,
          source: r.source,
        }));
        setRecommendations(transformed);
        const cuisineLabel = preferences.selectedCuisines.length > 0 ? preferences.selectedCuisines[0] : 'great';
        setUserPreference(
          `Hi ${user?.name || 'there'}! Based on your preference for ${preferences.selectedDiningType || 'casual'} ${cuisineLabel} dining in ${preferences.city} - ${preferences.locality}, with ${
            preferences.additionalDetails || 'a cozy vibe and outdoor seating'
          }, I found these places you might love!`
        );
      } else {
        setError('No restaurants found matching your preferences. Try adjusting your filters.');
      }
    } catch (err) {
      setError(
        axios.isAxiosError(err)
          ? err.response?.data?.detail || err.message
          : 'An error occurred while fetching recommendations'
      );
      setRecommendations([]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isLoaded || !user) return null;

  return (
    <>
      <Header cities={availableCities} city={selectedCity} onCityChange={setSelectedCity} userName={user.name} onLogout={logout} />
      <main className="bg-gradient-to-br from-red-50 to-red-100 min-h-screen">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">Discover Amazing Restaurants</h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              AI-powered recommendations tailored to your taste and budget
            </p>
          </div>

          {error && (
            <div className="mb-8 p-4 bg-red-50 border-l-4 border-red-600 rounded-lg">
              <p className="text-red-900 font-medium"><span className="font-bold">Error:</span> {error}</p>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div className="lg:col-span-4">
              <PreferenceForm
                onSubmit={handleSubmit}
                isLoading={isLoading}
                city={selectedCity}
                cities={availableCities}
                localities={localities}
                setCity={setSelectedCity}
              />
            </div>
            <div className="lg:col-span-8">
              <RecommendationsContainer
                recommendations={recommendations}
                isLoading={isLoading}
                userPreference={userPreference}
                userName={user.name}
              />
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
