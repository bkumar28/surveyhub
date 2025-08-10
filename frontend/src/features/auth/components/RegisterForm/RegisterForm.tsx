import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGoogle, faFacebook, faGithub } from '@fortawesome/free-brands-svg-icons';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '../../../../app/store';
import { register as registerUser } from '../../authSlice';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './RegisterForm.module.scss';

interface RegisterFormProps {
  onSuccess?: () => void;
}

interface RegisterFormData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  termsAccepted: boolean;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess }) => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [registerError, setRegisterError] = useState<string | null>(null);
  const [passwordStrength, setPasswordStrength] = useState({ score: 0, label: '' });

  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterFormData>();
  const password = watch('password', '');

  useEffect(() => {
    if (password) {
      // Password strength calculation
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

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setRegisterError(null);

    try {
      await dispatch(registerUser({
        firstName: data.firstName,
        lastName: data.lastName,
        email: data.email,
        password: data.password
      })).unwrap();

      if (onSuccess) {
        onSuccess();
      } else {
        // Redirect to login or verification page
        navigate('/login', { state: { registered: true } });
      }
    } catch (error) {
      setRegisterError(
        error instanceof Error
          ? error.message
          : 'Registration failed. Please try again.'
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
      {registerError && (
        <div className={styles.authError}>
          <p>{registerError}</p>
        </div>
      )}

      <div className={styles.formRow}>
        <div className={styles.formGroup}>
          <label htmlFor="firstName" className={styles.formLabel}>
            <span className={styles.requiredField}>First Name</span>
          </label>
          <input
            id="firstName"
            type="text"
            className={styles.formControl}
            placeholder="Enter your first name"
            {...register('firstName', {
              required: 'First name is required',
              maxLength: {
                value: 50,
                message: 'First name cannot exceed 50 characters'
              }
            })}
          />
          {errors.firstName && (
            <div className={styles.invalidFeedback}>{errors.firstName.message}</div>
          )}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="lastName" className={styles.formLabel}>
            <span className={styles.requiredField}>Last Name</span>
          </label>
          <input
            id="lastName"
            type="text"
            className={styles.formControl}
            placeholder="Enter your last name"
            {...register('lastName', {
              required: 'Last name is required',
              maxLength: {
                value: 50,
                message: 'Last name cannot exceed 50 characters'
              }
            })}
          />
          {errors.lastName && (
            <div className={styles.invalidFeedback}>{errors.lastName.message}</div>
          )}
        </div>
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="email" className={styles.formLabel}>
          <span className={styles.requiredField}>Email</span>
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
          <span className={styles.requiredField}>Password</span>
        </label>
        <div className={styles.passwordWrapper}>
          <input
            id="password"
            type={showPassword ? 'text' : 'password'}
            className={styles.formControl}
            placeholder="Create a password"
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
            placeholder="Confirm your password"
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

      <div className={styles.termsCheck}>
        <input
          id="termsAccepted"
          type="checkbox"
          className={styles.checkbox}
          {...register('termsAccepted', {
            required: 'You must accept the Terms and Conditions'
          })}
        />
        <label htmlFor="termsAccepted" className={styles.checkboxLabel}>
          I agree to the <Link to="/terms">Terms of Service</Link> and <Link to="/privacy">Privacy Policy</Link>
        </label>
      </div>
      {errors.termsAccepted && (
        <div className={styles.invalidFeedback}>{errors.termsAccepted.message}</div>
      )}

      <Button
        type="submit"
        className={styles.submitButton}
        isLoading={isLoading}
        disabled={isLoading}
      >
        Create Account
      </Button>

      <div className={styles.divider}>or</div>

      <div className={styles.socialLogin}>
        <button type="button" className={styles.socialButton}>
          <FontAwesomeIcon icon={faGoogle} />
          <span>Google</span>
        </button>
        <button type="button" className={styles.socialButton}>
          <FontAwesomeIcon icon={faFacebook} />
          <span>Facebook</span>
        </button>
        <button type="button" className={styles.socialButton}>
          <FontAwesomeIcon icon={faGithub} />
          <span>GitHub</span>
        </button>
      </div>

      <div className={styles.formFooter}>
        Already have an account? <Link to="/login">Sign in</Link>
      </div>
    </form>
  );
};

export default RegisterForm;
