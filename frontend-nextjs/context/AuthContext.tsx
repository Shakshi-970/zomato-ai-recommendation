'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8080';

interface User {
  name: string;
  email: string;
  token: string;
}

interface AuthContextType {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
  isLoaded: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  login: () => {},
  logout: () => {},
  isLoaded: false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Validate stored token against the backend on every page load.
    // If the token is invalid (server restarted with old in-memory sessions,
    // or token was manually tampered), clear it and send the user to login.
    const verifySession = async () => {
      try {
        const stored = localStorage.getItem('zomato_user');
        if (!stored) return;

        const parsed: User = JSON.parse(stored);
        const res = await fetch(`${API_BASE_URL}/auth/me?token=${encodeURIComponent(parsed.token)}`);

        if (res.ok) {
          setUser(parsed);
        } else {
          // Token rejected by server — clear stale session
          localStorage.removeItem('zomato_user');
        }
      } catch {
        // Network error: keep the stored session so the user isn't
        // unexpectedly logged out when the backend is temporarily unreachable.
        try {
          const stored = localStorage.getItem('zomato_user');
          if (stored) setUser(JSON.parse(stored));
        } catch {}
      } finally {
        setIsLoaded(true);
      }
    };

    verifySession();
  }, []);

  const login = (userData: User) => {
    setUser(userData);
    localStorage.setItem('zomato_user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('zomato_user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoaded }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
