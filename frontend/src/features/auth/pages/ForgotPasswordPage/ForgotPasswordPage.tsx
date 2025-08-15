import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../../app/store';
import { AuthLayout } from '../../../../shared/components/Layout/AuthLayout/AuthLayout';
import { ForgotPasswordForm } from '../../components/ForgotPasswordForm';

export const ForgotPasswordPage: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);

  // Redirect to dashboard if already authenticated
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <AuthLayout
      title="Reset Your Password"
      subtitle="Don't worry, it happens to the best of us. We'll help you get back into your account."
    >
      <ForgotPasswordForm />
    </AuthLayout>
  );
};

export default ForgotPasswordPage;
