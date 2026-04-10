'use client';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-red-600 rounded-full border-t-transparent border-r-transparent animate-spin"></div>
      </div>
      <p className="mt-6 text-lg text-gray-700 font-semibold">🍽️ Finding your perfect restaurants...</p>
      <p className="mt-2 text-sm text-gray-500">This may take a few seconds</p>
    </div>
  );
}
