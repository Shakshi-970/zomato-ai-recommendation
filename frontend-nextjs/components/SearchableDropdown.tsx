'use client';

import { useState, useRef, useEffect } from 'react';

interface SearchableDropdownProps {
  options: string[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  icon?: string;
}

export default function SearchableDropdown({
  options,
  value,
  onChange,
  placeholder = 'Search...',
  icon = '📍',
}: SearchableDropdownProps) {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = query.trim()
    ? options.filter((o) => o.toLowerCase().startsWith(query.trim().toLowerCase()))
    : options;

  // Close on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
        setQuery('');
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const select = (option: string) => {
    onChange(option);
    setQuery('');
    setOpen(false);
  };

  const handleFocus = () => {
    setOpen(true);
    setQuery('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setOpen(false);
      setQuery('');
    }
    if (e.key === 'Enter' && filtered.length > 0) {
      select(filtered[0]);
    }
  };

  return (
    <div ref={containerRef} className="relative w-full">
      {/* Input trigger */}
      <div
        className={`w-full flex items-center gap-2 rounded-2xl border bg-gray-50 px-4 py-3 cursor-text shadow-sm transition-all ${
          open ? 'border-red-500 ring-2 ring-red-100' : 'border-gray-200'
        }`}
        onClick={() => { setOpen(true); inputRef.current?.focus(); }}
      >
        <span className="text-base shrink-0">{icon}</span>
        <input
          ref={inputRef}
          type="text"
          value={open ? query : value}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={handleFocus}
          onKeyDown={handleKeyDown}
          placeholder={open ? `Type to search...` : placeholder}
          className="flex-1 bg-transparent text-sm text-gray-900 placeholder-gray-400 focus:outline-none"
        />
        <span
          className={`text-gray-400 text-xs transition-transform duration-200 shrink-0 ${open ? 'rotate-180' : ''}`}
        >
          ▼
        </span>
      </div>

      {/* Dropdown */}
      {open && (
        <div className="absolute z-50 mt-2 w-full bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden">
          {/* Search results count */}
          {query.trim() && (
            <div className="px-4 py-2 bg-red-50 border-b border-red-100">
              <span className="text-xs text-red-600 font-medium">
                {filtered.length} result{filtered.length !== 1 ? 's' : ''} for "{query}"
              </span>
            </div>
          )}

          <ul className="max-h-60 overflow-y-auto py-1">
            {filtered.length > 0 ? (
              filtered.map((option) => {
                const matchIndex = option.toLowerCase().indexOf(query.trim().toLowerCase());
                const isMatch = query.trim() && matchIndex !== -1;
                return (
                  <li
                    key={option}
                    onClick={() => select(option)}
                    className={`flex items-center gap-3 px-4 py-2.5 cursor-pointer text-sm transition-colors hover:bg-red-50 group ${
                      option === value ? 'bg-red-50 text-red-700 font-semibold' : 'text-gray-700'
                    }`}
                  >
                    <span className="text-xs text-gray-300 group-hover:text-red-300">📍</span>
                    {isMatch ? (
                      <span>
                        <span className="text-red-600 font-bold">
                          {option.slice(matchIndex, matchIndex + query.trim().length)}
                        </span>
                        {option.slice(matchIndex + query.trim().length)}
                      </span>
                    ) : (
                      <span>{option}</span>
                    )}
                    {option === value && (
                      <span className="ml-auto text-red-500 text-xs">✓</span>
                    )}
                  </li>
                );
              })
            ) : (
              <li className="px-4 py-6 text-center text-sm text-gray-400">
                No locations found for "{query}"
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
