import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../api/types';
import { authApi } from '../api/auth';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          const userData = await authApi.getMe();
          setUser(userData);
        } catch (error) {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authApi.login({ email, password });
      localStorage.setItem('auth_token', response.access_token);
      
      const userData = await authApi.getMe();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      toast.success('Успешный вход в систему!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Ошибка входа');
      throw error;
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    try {
      const response = await authApi.register({ email, password, name });
      localStorage.setItem('auth_token', response.access_token);
      
      const userData = await authApi.getMe();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      toast.success('Регистрация прошла успешно!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Ошибка регистрации');
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setUser(null);
    toast.success('Вы вышли из системы');
  };

  const value: AuthContextType = {
    user,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

