import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '../../../../app/store';
import { resetPassword } from '../../authSlice';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './ResetPasswordForm.module.scss';

interface ResetPasswordFormProps {
  token: string;
  onSuccess?: () => void;
  hideHeader?: boolean;
}

interface ResetPasswordFormData {
  password: string;
  confirmPassword: string;
}

export const ResetPasswordForm: React.FC<ResetPasswordFormProps> = ({
  token,
  onSuccess,
  hideHeader = false
}) => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<'weak' | 'medium' | 'strong' | ''>('');

  const { register, handleSubmit, watch, formState: { errors } } = useForm<ResetPasswordFormData>();
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

  const onSubmit = async (data: ResetPasswordFormData) => {
    if (data.password !== data.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await dispatch(resetPassword({
        token: token,
        password: data.password
      })).unwrap();

      setIsSubmitted(true);

      if (onSuccess) {
        onSuccess();
      } else {
        // Redirect to login after 3 seconds
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      }
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Failed to reset password. The link may have expired or is invalid.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className={styles.successMessage}>
        <p><strong>Password reset successful!</strong></p>
        <p>
          Your password has been successfully changed. You can now log in with your new password.
        </p>
        <p>
          You will be redirected to the login page automatically, or you can click the button below.
        </p>
        <div className={styles.actionButtons}>
          <Button
            onClick={() => navigate('/login')}
            className={styles.submitButton}
          >
            Go to Login
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.formWrapper}>
      {!hideHeader && (
        <>
          <h2 className={styles.formTitle}>Reset Password</h2>
          <p className={styles.formSubtitle}>Create a new secure password for your account</p>
        </>
      )}

      <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
        {error && (
          <div className={styles.authError}>
            <p>{error}</p>
          </div>
        )}

        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.formLabel}>
            <span className={styles.requiredField}>New Password</span>
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

        <div className={styles.actionButtons}>
          <Link to="/login" className={styles.backButton}>
            Back to login
          </Link>
          <Button
            type="submit"
            className={styles.submitButton}
            isLoading={isLoading}
            disabled={isLoading}
          >
            Reset Password
          </Button>
        </div>
      </form>
    </div>
  );
};
