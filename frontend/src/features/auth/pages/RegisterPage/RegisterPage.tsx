import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../../app/store';
import { AuthLayout } from '../../../../shared/components/Layout/AuthLayout/AuthLayout';
import { RegisterForm } from '../../components/RegisterForm/RegisterForm';

export const RegisterPage: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <AuthLayout
      title="Create an Account"
      subtitle="Join SurveyHub today and start creating engaging surveys"
    >
      <RegisterForm />
    </AuthLayout>
  );
};

export default RegisterPage;
