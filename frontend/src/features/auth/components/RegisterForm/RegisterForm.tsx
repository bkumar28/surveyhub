import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '../../../../app/store';
import { register as registerUser } from '../../authSlice'; // Renamed to avoid conflict with useForm's register
import styles from './RegisterForm.module.scss';

interface RegisterFormProps {
  onSuccess?: () => void;
  hideHeader?: boolean;
}

interface RegisterFormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  agreeToTerms: boolean;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({
  onSuccess,
  hideHeader = false
}) => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<'weak' | 'medium' | 'strong' | ''>('');

  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterFormData>({
    defaultValues: {
      agreeToTerms: false
    }
  });

  const password = watch('password', '');

  // Check password strength when it changes
  React.useEffect(() => {
    if (!password) {
      setPasswordStrength('');
      return;
    }

    // Basic password strength check
    const hasLowerCase = /[a-z]/.test(password);
    const hasUpperCase = /[A-Z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChars = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password);
    const isLongEnough = password.length >= 8;

    const passedChecks = [hasLowerCase, hasUpperCase, hasNumbers, hasSpecialChars, isLongEnough].filter(Boolean).length;

    if (passedChecks <= 2) {
      setPasswordStrength('weak');
    } else if (passedChecks <= 4) {
      setPasswordStrength('medium');
    } else {
      setPasswordStrength('strong');
    }
  }, [password]);

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await dispatch(registerUser({
        name: data.name,
        email: data.email,
        password: data.password,
        confirmPassword: data.confirmPassword
      })).unwrap();

      if (onSuccess) {
        onSuccess();
      } else {
        navigate('/dashboard');
      }
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Failed to register. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.formWrapper}>
      {!hideHeader && (
        <>
          <h2 className={styles.formTitle}>Create an Account</h2>
          <p className={styles.formSubtitle}>Get started with SurveyHub</p>
        </>
      )}

      <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
        {error && (
          <div className={styles.authError}>
            <p>{error}</p>
          </div>
        )}

        <div className={styles.formGroup}>
          <label htmlFor="name" className={styles.formLabel}>
            <span className={styles.requiredField}>Full Name</span>
          </label>
          <input
            id="name"
            type="text"
            className={`${styles.formControl} ${errors.name ? styles.isInvalid : ''}`}
            placeholder="John Doe"
            {...register('name', {
              required: 'Name is required',
              minLength: {
                value: 2,
                message: 'Name must be at least 2 characters long'
              }
            })}
          />
          {errors.name && (
            <div className={styles.invalidFeedback}>{errors.name.message}</div>
          )}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="email" className={styles.formLabel}>
            <span className={styles.requiredField}>Email Address</span>
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

        {/* Password field with strength indicator */}
        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.formLabel}>
            <span className={styles.requiredField}>Password</span>
          </label>
          <div className={styles.passwordWrapper}>
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              className={`${styles.formControl} ${errors.password ? styles.isInvalid : ''}`}
              placeholder="••••••••"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 8,
                  message: 'Password must be at least 8 characters long'
                },
                pattern: {
                  value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?])[A-Za-z\d!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]{8,}$/,
                  message: 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
                }
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

          {password && (
            <div className={styles.passwordStrength}>
              <div className={`${styles.passwordStrengthText} ${styles[passwordStrength]}`}>
                {passwordStrength === 'weak' && 'Weak Password'}
                {passwordStrength === 'medium' && 'Medium Password'}
                {passwordStrength === 'strong' && 'Strong Password'}
              </div>
              <div className={styles.passwordStrengthBar}>
                <div className={`${styles.progress} ${styles[passwordStrength]}`}></div>
              </div>

              <div className={styles.passwordRequirements}>
                Password requirements:
                <ul>
                  <li className={/[a-z]/.test(password) ? styles.valid : ''}>
                    <FontAwesomeIcon icon={/[a-z]/.test(password) ? faCheck : faTimes} />{' '}
                    One lowercase letter
                  </li>
                  <li className={/[A-Z]/.test(password) ? styles.valid : ''}>
                    <FontAwesomeIcon icon={/[A-Z]/.test(password) ? faCheck : faTimes} />{' '}
                    One uppercase letter
                  </li>
                  <li className={/\d/.test(password) ? styles.valid : ''}>
                    <FontAwesomeIcon icon={/\d/.test(password) ? faCheck : faTimes} />{' '}
                    One number
                  </li>
                  <li className={/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password) ? styles.valid : ''}>
                    <FontAwesomeIcon icon={/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password) ? faCheck : faTimes} />{' '}
                    One special character
                  </li>
                  <li className={password.length >= 8 ? styles.valid : ''}>
                    <FontAwesomeIcon icon={password.length >= 8 ? faCheck : faTimes} />{' '}
                    At least 8 characters
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="confirmPassword" className={styles.formLabel}>
            <span className={styles.requiredField}>Confirm Password</span>
          </label>
          <div className={styles.passwordWrapper}>
            <input
              id="confirmPassword"
              type={showConfirmPassword ? 'text' : 'password'}
              className={`${styles.formControl} ${errors.confirmPassword ? styles.isInvalid : ''}`}
              placeholder="••••••••"
              {...register('confirmPassword', {
                required: 'Please confirm your password',
                validate: value => value === password || 'Passwords do not match'
              })}
            />
            <button
              type="button"
              className={styles.passwordToggle}
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
            >
              <FontAwesomeIcon icon={showConfirmPassword ? faEyeSlash : faEye} />
            </button>
          </div>
          {errors.confirmPassword && (
            <div className={styles.invalidFeedback}>{errors.confirmPassword.message}</div>
          )}
        </div>

        <div className={styles.formCheck}>
          <input
            id="agreeToTerms"
            type="checkbox"
            className={styles.formCheckInput}
            {...register('agreeToTerms', {
              required: 'You must agree to the terms and privacy policy'
            })}
          />
          <label htmlFor="agreeToTerms" className={styles.formCheckLabel}>
            I agree to the <Link to="/terms">Terms of Service</Link> and <Link to="/privacy">Privacy Policy</Link>
          </label>
          {errors.agreeToTerms && (
            <div className={styles.invalidFeedback}>{errors.agreeToTerms.message}</div>
          )}
        </div>

        <button
          type="submit"
          className={styles.submitButton}
          disabled={isLoading}
        >
          {isLoading ? (
            <span className={styles.loadingSpinner}></span>
          ) : (
            "Create Account"
          )}
        </button>
      </form>

      <div className={styles.divider}>
        <span>OR</span>
      </div>

      <div className={styles.socialLogin}>
        <button className={styles.googleButton} type="button">
          <i className="fab fa-google"></i>
          Sign up with Google
        </button>
      </div>

      <div className={styles.formFooter}>
        <p>Already have an account? <Link to="/login">Sign in</Link></p>
      </div>
    </div>
  );
};
