import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { useAppDispatch } from '../../../../app/store';
import { forgotPassword } from '../../authSlice';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './ForgotPasswordForm.module.scss';

interface ForgotPasswordFormProps {
  onSuccess?: () => void;
}

interface ForgotPasswordFormData {
  email: string;
}

export const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({ onSuccess }) => {
  const dispatch = useAppDispatch();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<ForgotPasswordFormData>();

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await dispatch(forgotPassword({ email: data.email })).unwrap();
      setIsSubmitted(true);

      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Failed to process your request. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className={styles.successMessage}>
        <p><strong>Password reset email sent!</strong></p>
        <p>
          We've sent an email to the address you provided with instructions to reset your password.
          Please check your inbox and follow the link in the email.
        </p>
        <p>
          If you don't receive an email within a few minutes, please check your spam folder or try again.
        </p>
      </div>
    );
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      {error && (
        <div className={styles.authError}>
          <p>{error}</p>
        </div>
      )}

      <div className={styles.instructions}>
        Enter your email address and we'll send you a link to reset your password.
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
          Send Reset Link
        </Button>
      </div>
    </form>
  );
};

export default ForgotPasswordForm;
