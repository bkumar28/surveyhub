import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash, faExclamationCircle } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '../../../../app/store';
import { login } from '../../authSlice';
import styles from './LoginForm.module.scss';

interface LoginFormProps {
  onSuccess?: () => void;
  hideHeader?: boolean;
}

interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onSuccess,
  hideHeader = false
}) => {
  const dispatch = useAppDispatch();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    defaultValues: {
      rememberMe: false
    }
  });

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

  return (
    <div className={styles.formWrapper}>
      {loginError && (
        <div className={styles.errorAlert}>
          <FontAwesomeIcon icon={faExclamationCircle} className={styles.errorIcon} />
          <span>{loginError}</span>
        </div>
      )}

      {/* Only show the form header if not hidden */}
      {!hideHeader && (
        <>
          <h2 className={styles.formTitle}>Sign In</h2>
          <p className={styles.formSubtitle}>Enter your credentials to access your account</p>
        </>
      )}

      <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.formGroup}>
          <label htmlFor="email" className={styles.formLabel}>
            Email Address
          </label>
          <input
            id="email"
            type="email"
            className={`${styles.formControl} ${errors.email ? styles.isInvalid : ''}`}
            placeholder="name@company.com"
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
          <div className={styles.labelFlex}>
            <label htmlFor="password" className={styles.formLabel}>
              Password
            </label>
            <Link to="/forgot-password" className={styles.forgotPassword}>
              Forgot password?
            </Link>
          </div>
          <div className={styles.passwordWrapper}>
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              className={`${styles.formControl} ${errors.password ? styles.isInvalid : ''}`}
              placeholder="••••••••"
              {...register('password', {
                required: 'Password is required'
              })}
            />
            <button
              type="button"
              className={styles.passwordToggle}
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
            </button>
          </div>
          {errors.password && (
            <div className={styles.invalidFeedback}>{errors.password.message}</div>
          )}
        </div>

        <div className={styles.formCheck}>
          <input
            id="rememberMe"
            type="checkbox"
            className={styles.formCheckInput}
            {...register('rememberMe')}
          />
          <label htmlFor="rememberMe" className={styles.formCheckLabel}>
            Remember me
          </label>
        </div>

        <button
          type="submit"
          className={styles.submitButton}
          disabled={isLoading}
        >
          {isLoading ? (
            <span className={styles.loadingSpinner}></span>
          ) : (
            "Sign in"
          )}
        </button>
      </form>

      <div className={styles.divider}>
        <span>OR</span>
      </div>

      <div className={styles.socialLogin}>
        <button className={styles.googleButton} type="button">
          <i className="fab fa-google"></i>
          Sign in with Google
        </button>
      </div>

      <div className={styles.formFooter}>
        <p>Don't have an account? <Link to="/register">Sign up</Link></p>
      </div>

      {/* Mobile features section - only visible on small screens */}
      <div className={styles.mobileFeatures}>
        <p className={styles.mobileFeaturesText}>SurveyHub helps you:</p>
        <ul className={styles.mobileFeaturesList}>
          <li className={styles.mobileFeatureItem}>
            <i className="fas fa-chart-bar"></i>
            <span>Create surveys with powerful analytics</span>
          </li>
          <li className={styles.mobileFeatureItem}>
            <i className="fas fa-mobile-alt"></i>
            <span>Design responsive surveys for any device</span>
          </li>
          <li className={styles.mobileFeatureItem}>
            <i className="fas fa-lock"></i>
            <span>Keep your data secure and private</span>
          </li>
        </ul>
      </div>
    </div>
  );
};
