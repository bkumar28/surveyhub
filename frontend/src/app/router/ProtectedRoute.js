import React from 'react';
import { Navigate } from 'react-router-dom';
import { AppLayout } from '../../shared/components/layout';

export const ProtectedRoute = ({ children, isAuthenticated }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <AppLayout>{children}</AppLayout>;
};
