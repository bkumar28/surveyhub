import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store, useAppDispatch } from './app/store';
import { restoreAuth } from './features/auth/authSlice';
import { AppLayout } from './shared/components/Layout/AppLayout';

// Import route protection components
import { PublicRoute, ProtectedRoute } from './shared/components/Routes';

// Import all auth pages
import { LoginPage } from './features/auth/pages/LoginPage/LoginPage';
import { RegisterPage } from './features/auth/pages/RegisterPage/RegisterPage';
import { ForgotPasswordPage } from './features/auth/pages/ForgotPasswordPage/ForgotPasswordPage';
import { ResetPasswordPage } from './features/auth/pages/ResetPasswordPage/ResetPasswordPage';

import { DashboardPage } from './features/dashboard/pages/DashboardPage';
import { SurveysPage } from './features/surveys/pages/SurveysPage';
import './assets/styles/main.scss';

const AppContent: React.FC = () => {
  // Add this effect to restore authentication state from localStorage/sessionStorage
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(restoreAuth());
  }, [dispatch]);

  return (
    <Router>
      <Routes>
        {/* Public auth routes */}
        <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />
        <Route path="/forgot-password" element={<PublicRoute><ForgotPasswordPage /></PublicRoute>} />
        <Route path="/reset-password/:token" element={<PublicRoute><ResetPasswordPage /></PublicRoute>} />

        {/* Protected routes */}
        <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="surveys" element={<SurveysPage />} />
          <Route path="users" element={<div>Users Page - Coming Soon</div>} />
          <Route path="analytics" element={<div>Analytics Page - Coming Soon</div>} />
          <Route path="settings" element={<div>Settings Page - Coming Soon</div>} />
        </Route>

        {/* Catch-all route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

function App() {
  return (
    <Provider store={store}>
      <AppContent />
    </Provider>
  );
}

export default App;
