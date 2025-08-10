import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../../app/store';
import { AuthLayout } from '../../../../shared/components/Layout/AuthLayout/AuthLayout';
import { ForgotPasswordForm } from '../../components/ForgotPasswordForm/ForgotPasswordForm';

export const ForgotPasswordPage: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <AuthLayout
      title="Forgot Password"
      subtitle="Enter your email and we'll send you a link to reset your password"
    >
      <ForgotPasswordForm />
    </AuthLayout>
  );
};

export default ForgotPasswordPage;
