'use client';

interface HeaderProps {
  cities: string[];
  city: string;
  onCityChange: (city: string) => void;
  userName?: string;
  onLogout?: () => void;
}

export default function Header({ cities, city, onCityChange, userName, onLogout }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50 backdrop-blur-lg bg-white/95">
      <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col lg:flex-row items-center gap-4 lg:gap-6">
        <div className="flex items-center">
          <span className="text-3xl font-black tracking-tight text-slate-950 leading-none" style={{ letterSpacing: '-0.03em' }}>
            zomato
          </span>
        </div>

        <div className="flex items-center gap-3 rounded-full border border-gray-200 bg-gray-50 px-4 py-2 shadow-sm">
          <span className="text-lg">📍</span>
          <select
            value={city}
            onChange={(e) => onCityChange(e.target.value)}
            className="bg-transparent text-sm font-medium text-gray-900 focus:outline-none"
          >
            {cities.length ? (
              cities.map((c) => <option key={c} value={c}>{c}</option>)
            ) : (
              <option value="">No supported cities</option>
            )}
          </select>
          <span className="text-gray-400">▼</span>
        </div>

        <div className="flex-1 min-w-[300px]">
          <div className="relative">
            <input
              type="text"
              placeholder="Search for restaurants, cuisines, dishes..."
              className="w-full rounded-full border border-gray-200 bg-white px-5 py-3 pr-12 text-sm text-gray-800 shadow-sm focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-200 transition-all"
            />
            <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {userName && (
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-gradient-to-br from-red-500 to-red-700 rounded-full flex items-center justify-center text-white font-bold text-sm shadow">
                {userName.charAt(0).toUpperCase()}
              </div>
              <span className="text-sm font-semibold text-gray-800 hidden lg:block">{userName}</span>
            </div>
          )}
          {onLogout && (
            <button
              onClick={onLogout}
              className="text-sm font-medium text-gray-600 hover:text-red-600 border border-gray-200 rounded-full px-4 py-2 hover:border-red-300 transition-all"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
