import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAppSelector } from '../../../app/store';

interface PublicRouteProps {
  children: React.ReactNode;
  redirectAuthenticated?: boolean;
}

export const PublicRoute: React.FC<PublicRouteProps> = ({
  children,
  redirectAuthenticated = true
}) => {
  const { isAuthenticated, loading } = useAppSelector(state => state.auth);
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  // Show loading state while authentication status is being checked
  if (loading) {
    return <div className="auth-loading">Loading...</div>;
  }

  // Redirect to dashboard if authenticated and redirect is enabled
  if (isAuthenticated && redirectAuthenticated) {
    return <Navigate to={from} replace />;
  }

  // Render children if not authenticated or redirect is disabled
  return <>{children}</>;
};
