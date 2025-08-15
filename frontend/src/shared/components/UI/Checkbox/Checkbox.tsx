import React from 'react';
import styles from './Checkbox.module.scss';

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label: string;
  error?: string;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className = '', label, error, ...props }, ref) => {
    return (
      <div className={`${styles.checkboxWrapper} ${className}`}>
        <label className={styles.label}>
          <input
            ref={ref}
            type="checkbox"
            className={`
              ${styles.checkbox}
              ${error ? styles.checkboxError : ''}
              ${props.disabled ? styles.checkboxDisabled : ''}
            `}
            {...props}
          />
          <span className={styles.checkmark}></span>
          <span className={styles.labelText}>{label}</span>
        </label>
        {error && <div className={styles.errorMessage}>{error}</div>}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';
