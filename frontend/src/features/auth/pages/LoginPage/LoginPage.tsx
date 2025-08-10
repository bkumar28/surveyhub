import React from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../../app/store';
import { AuthLayout } from '../../../../shared/components/Layout/AuthLayout/AuthLayout';
import { LoginForm } from '../../components/LoginForm/LoginForm';

export const LoginPage: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);
  const location = useLocation();
  const redirectTo = location.state?.from?.pathname || '/dashboard';

  if (isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  return (
    <AuthLayout
      title="Sign In to SurveyHub"
      subtitle="Welcome back! Please enter your details to access your account"
    >
      <LoginForm />
    </AuthLayout>
  );
};

export default LoginPage;
