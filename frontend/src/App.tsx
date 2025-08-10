import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store, useAppDispatch, useAppSelector } from './app/store';
import { restoreAuth } from './features/auth/authSlice';
import { AppLayout } from './shared/components/Layout/AppLayout';
import { AuthLayout } from './shared/components/Layout/AuthLayout';
import { LoginPage } from './features/auth/pages/LoginPage';
import { DashboardPage } from './features/dashboard/pages/DashboardPage';
import { SurveysPage } from './features/surveys/pages/SurveysPage';
import './assets/styles/main.scss';

// Enhanced ProtectedRoute that only redirects for true auth errors
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const dispatch = useAppDispatch();
  const location = useLocation();
  const { isAuthenticated, loading } = useAppSelector((state) => state.auth);

  // Check for token in localStorage
  const token = localStorage.getItem('access_token');

  useEffect(() => {
    dispatch(restoreAuth());
  }, [dispatch, isAuthenticated, loading, token]);

  // Show loading indicator while checking authentication
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  // Only redirect if there's no token at all
  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // Otherwise show the protected content, even if APIs fail with 404/500
  return <>{children}</>;
};

// Public route - redirect to dashboard if already authenticated
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  const token = localStorage.getItem('access_token');

  if (isAuthenticated || token) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

const AppContent: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <AuthLayout>
                <LoginPage />
              </AuthLayout>
            </PublicRoute>
          }
        />
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
