import React from 'react';
import { useParams, Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../../app/store';
import { AuthLayout } from '../../../../shared/components/Layout/AuthLayout/AuthLayout';
import { ResetPasswordForm } from '../../components/ResetPasswordForm/ResetPasswordForm';

export const ResetPasswordPage: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const { isAuthenticated } = useAppSelector(state => state.auth);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  if (!token) {
    return <Navigate to="/forgot-password" replace />;
  }

  return (
    <AuthLayout
      title="Create New Password"
      subtitle="Enter a new password for your SurveyHub account"
    >
      <ResetPasswordForm token={token} />
    </AuthLayout>
  );
};

export default ResetPasswordPage;
