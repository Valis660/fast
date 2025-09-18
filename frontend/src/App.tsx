import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout/Layout';
import HomePage from './pages/HomePage';
import HotelDetailPage from './pages/HotelDetailPage';
import MyBookingsPage from './pages/MyBookingsPage';
import LoginForm from './components/Auth/LoginForm';
import RegisterForm from './components/Auth/RegisterForm';

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        
        {/* Защищенные маршруты */}
        <Route path="/" element={<Layout><Outlet /></Layout>}>
          <Route index element={<HomePage />} />
          <Route path="hotels/:id" element={<HotelDetailPage />} />
          <Route path="my-bookings" element={<MyBookingsPage />} />
        </Route>
        
        {/* Редирект на главную */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Toaster position="top-right" />
    </AuthProvider>
  );
}

export default App;