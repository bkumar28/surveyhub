import React from 'react';
import { Navigate } from 'react-router-dom';
import { AuthLayout } from '../../shared/components/layout';

export const PublicRoute = ({ children, isAuthenticated }) => {
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <AuthLayout>{children}</AuthLayout>;
};
