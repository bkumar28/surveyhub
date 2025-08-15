import React from 'react';
import styles from './Spinner.module.scss';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark';
  fullScreen?: boolean;
  fullWidth?: boolean;
  className?: string;
  label?: string;
  srOnly?: boolean;
  testId?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  variant = 'primary',
  fullScreen = false,
  fullWidth = false,
  className = '',
  label = 'Loading...',
  srOnly = true,
  testId,
}) => {
  const spinnerElement = (
    <div
      className={`
        ${styles.spinner}
        ${styles[`spinner-${size}`]}
        ${styles[`spinner-${variant}`]}
        ${fullWidth ? styles.fullWidth : ''}
        ${className}
      `}
      role="status"
      data-testid={testId}
    >
      <span className={srOnly ? styles.srOnly : undefined}>{label}</span>
    </div>
  );

  if (fullScreen) {
    return (
      <div className={styles.fullScreenWrapper}>
        {spinnerElement}
      </div>
    );
  }

  return spinnerElement;
};
