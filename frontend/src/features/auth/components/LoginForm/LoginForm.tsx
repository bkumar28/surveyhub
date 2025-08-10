import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '../../../../app/store';
import { login } from '../../authSlice';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './LoginForm.module.scss';

interface LoginFormProps {
  onSuccess?: () => void;
}

interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const dispatch = useAppDispatch();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>();

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setLoginError(null);

    try {
      await dispatch(login({
        email: data.email,
        password: data.password,
        rememberMe: data.rememberMe
      })).unwrap();

      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      setLoginError(
        error instanceof Error
          ? error.message
          : 'Failed to login. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(prev => !prev);
  };

  return (
    <div className={styles.formWrapper}>
      <div className={styles.topText}>
        <p className={styles.leadText}>Sign in to your account to continue</p>
      </div>

      <div className={styles.cardShadow}>
        <div className={styles.cardBody}>
          <div className={styles.cardContent}>
            <div className={styles.formHeader}>
              <h2 className={styles.logo}>
                <span className={styles.logoTextPrimary}>Survey</span>
                <span className={styles.logoTextAccent}>Hub</span>
              </h2>
              <h3 className={styles.welcomeText}>Welcome back</h3>
            </div>

            {loginError && (
              <div className={styles.authError}>
                <p>{loginError}</p>
              </div>
            )}

            <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
              <div className={styles.formGroup}>
                <label htmlFor="email" className={styles.formLabel}>
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  className={styles.formControl}
                  placeholder="Enter your email"
                  {...register('email', {
                    required: 'Email is required',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Invalid email address'
                    }
                  })}
                />
                {errors.email && (
                  <div className={styles.invalidFeedback}>{errors.email.message}</div>
                )}
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="password" className={styles.formLabel}>
                  Password
                </label>
                <div className={styles.passwordWrapper}>
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    className={styles.formControl}
                    placeholder="Enter your password"
                    {...register('password', {
                      required: 'Password is required'
                    })}
                  />
                  <button
                    type="button"
                    className={styles.passwordToggle}
                    onClick={togglePasswordVisibility}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
                  </button>
                </div>
                {errors.password && (
                  <div className={styles.invalidFeedback}>{errors.password.message}</div>
                )}
                <div className={styles.forgotPasswordWrapper}>
                  <Link to="/forgot-password" className={styles.forgotPassword}>
                    Forgot password?
                  </Link>
                </div>
              </div>

              <div className={styles.formGroup}>
                <div className={styles.checkboxWrapper}>
                  <input
                    id="rememberMe"
                    type="checkbox"
                    className={styles.checkbox}
                    {...register('rememberMe')}
                  />
                  <label htmlFor="rememberMe" className={styles.checkboxLabel}>
                    Remember me
                  </label>
                </div>
              </div>

              <div className={styles.submitButtonWrapper}>
                <Button
                  type="submit"
                  className={styles.submitButton}
                  isLoading={isLoading}
                  disabled={isLoading}
                >
                  Sign in
                </Button>
              </div>
            </form>

            <div className={styles.formFooter}>
              <p>Don't have an account? <Link to="/register">Sign up</Link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
