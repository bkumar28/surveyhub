import React from 'react';
import { Navigate, useSearchParams } from 'react-router-dom';
import { useAppSelector } from '../../../../app/store';
import { AuthLayout } from '../../../../shared/components/Layout/AuthLayout/AuthLayout';
import { ResetPasswordForm } from '../../components/ResetPasswordForm/ResetPasswordForm';

export const ResetPasswordPage: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  if (!token) {
    return <Navigate to="/forgot-password" replace />;
  }

  return (
    <AuthLayout
      title="Reset Password"
      subtitle="Create a new secure password for your account"
    >
      <ResetPasswordForm />
    </AuthLayout>
  );
};

export default ResetPasswordPage;
