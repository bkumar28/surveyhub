import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { ProtectedRoute } from './ProtectedRoute';
import { PublicRoute } from './PublicRoute';
import { LoadingSpinner } from '../../shared/components/feedback';

// Lazy load pages
const LoginPage = React.lazy(() => import('../../features/auth/pages/LoginPage'));
const DashboardPage = React.lazy(() => import('../../features/dashboard/pages/DashboardPage'));
const SurveyListPage = React.lazy(() => import('../../features/surveys/pages/SurveyListPage'));

export const AppRouter = () => {
  const { isAuthenticated } = useSelector((state) => state.auth);

  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        {/* Public Routes */}
        <Route
          path="/login"
          element={
            <PublicRoute isAuthenticated={isAuthenticated}>
              <LoginPage />
            </PublicRoute>
          }
        />

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/surveys"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <SurveyListPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Suspense>
  );
};
