'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

// Define types
interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => Promise<void>;
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProvider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Check authentication status on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      setIsLoading(true);
      // In a real app, this would make an API call to verify the session
      // For now, we'll just check if there's a user in localStorage
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
    } catch (err) {
      console.error('Error checking auth status:', err);
      setError('Failed to check authentication status');
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setError(null);

      // In a real app, this would make an API call to the backend
      // For now, we'll simulate a successful login
      const mockUser = {
        id: '1',
        email,
        name: email.split('@')[0] // Use part of email as name
      };

      // Save user to localStorage (in real app, handle JWT tokens properly)
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      setError('Login failed. Please check your credentials.');
      throw err;
    }
  };

  const signup = async (email: string, password: string, name?: string) => {
    try {
      setError(null);

      // In a real app, this would make an API call to the backend
      // For now, we'll simulate a successful signup
      const mockUser = {
        id: Date.now().toString(), // Mock ID
        email,
        name: name || email.split('@')[0]
      };

      // Save user to localStorage (in real app, handle JWT tokens properly)
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      setError('Signup failed. Please try again.');
      throw err;
    }
  };

  const logout = () => {
    // Clear user data from localStorage
    localStorage.removeItem('user');
    setUser(null);

    // Redirect to login
    router.push('/login');
  };

  const value: AuthContextType = {
    user,
    isLoggedIn: !!user,
    isLoading,
    error,
    login,
    signup,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}