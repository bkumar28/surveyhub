import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '../../../../app/store';
import { resetPassword } from '../../authSlice';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './ResetPasswordForm.module.scss';

interface ResetPasswordFormProps {
  onSuccess?: () => void;
}

interface ResetPasswordFormData {
  password: string;
  confirmPassword: string;
}

export const ResetPasswordForm: React.FC<ResetPasswordFormProps> = ({ onSuccess }) => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [resetError, setResetError] = useState<string | null>(null);
  const [passwordStrength, setPasswordStrength] = useState({ score: 0, label: '' });

  const { register, handleSubmit, watch, formState: { errors } } = useForm<ResetPasswordFormData>();
  const password = watch('password', '');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
  }, [token, navigate]);

  useEffect(() => {
    if (password) {
      // Simple password strength calculation - in a real app, use a more sophisticated approach
      const hasLower = /[a-z]/.test(password);
      const hasUpper = /[A-Z]/.test(password);
      const hasNumber = /[0-9]/.test(password);
      const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
      const length = password.length;

      let score = 0;
      if (length >= 8) score++;
      if (length >= 12) score++;
      if (hasLower) score++;
      if (hasUpper) score++;
      if (hasNumber) score++;
      if (hasSpecial) score++;

      let label = '';
      if (score <= 2) label = 'weak';
      else if (score <= 4) label = 'medium';
      else label = 'strong';

      setPasswordStrength({ score, label });
    } else {
      setPasswordStrength({ score: 0, label: '' });
    }
  }, [password]);

  const onSubmit = async (data: ResetPasswordFormData) => {
    if (!token) return;

    setIsLoading(true);
    setResetError(null);

    try {
      await dispatch(resetPassword({
        token,
        password: data.password
      })).unwrap();

      if (onSuccess) {
        onSuccess();
      } else {
        navigate('/login', { state: { message: 'Your password has been reset successfully. You can now login with your new password.' } });
      }
    } catch (error) {
      setResetError(
        error instanceof Error
          ? error.message
          : 'Failed to reset password. The link may be expired or invalid.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(prev => !prev);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(prev => !prev);
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      {resetError && (
        <div className={styles.authError}>
          <p>{resetError}</p>
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
            className={styles.formControl}
            placeholder="Enter your new password"
            {...register('password', {
              required: 'Password is required',
              minLength: {
                value: 8,
                message: 'Password must be at least 8 characters'
              },
              pattern: {
                value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\W]{8,}$/,
                message: 'Password must contain at least one uppercase letter, one lowercase letter, and one number'
              }
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

        {password && (
          <div className={styles.passwordStrength}>
            <div className={styles.strengthBar}>
              <div
                className={`${styles.strengthIndicator} ${styles[passwordStrength.label]}`}
                style={{ width: `${(passwordStrength.score / 6) * 100}%` }}
              ></div>
            </div>
            <div className={`${styles.strengthText} ${styles[passwordStrength.label]}`}>
              {passwordStrength.label === 'weak' && 'Weak password'}
              {passwordStrength.label === 'medium' && 'Medium strength password'}
              {passwordStrength.label === 'strong' && 'Strong password'}
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
            className={styles.formControl}
            placeholder="Confirm your new password"
            {...register('confirmPassword', {
              required: 'Please confirm your password',
              validate: value => value === password || "Passwords don't match"
            })}
          />
          <button
            type="button"
            className={styles.passwordToggle}
            onClick={toggleConfirmPasswordVisibility}
            aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
          >
            <FontAwesomeIcon icon={showConfirmPassword ? faEyeSlash : faEye} />
          </button>
        </div>
        {errors.confirmPassword && (
          <div className={styles.invalidFeedback}>{errors.confirmPassword.message}</div>
        )}
      </div>

      <Button
        type="submit"
        className={styles.submitButton}
        isLoading={isLoading}
        disabled={isLoading}
      >
        Reset Password
      </Button>
    </form>
  );
};

export default ResetPasswordForm;
