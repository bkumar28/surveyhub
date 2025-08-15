import React from 'react';
import styles from './Select.module.scss';

interface Option {
  value: string | number;
  label: string;
}

interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'onChange'> {
  options: Option[];
  error?: string;
  label?: string;
  fullWidth?: boolean;
  onChange?: (value: string) => void;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className = '', options, error, label, fullWidth = false, onChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
      if (onChange) {
        onChange(e.target.value);
      }
    };

    return (
      <div
        className={`
          ${styles.selectWrapper}
          ${fullWidth ? styles.fullWidth : ''}
          ${className}
        `}
      >
        {label && <label className={styles.label}>{label}</label>}
        <div className={styles.selectContainer}>
          <select
            ref={ref}
            className={`
              ${styles.select}
              ${error ? styles.selectError : ''}
              ${props.disabled ? styles.selectDisabled : ''}
            `}
            onChange={handleChange}
            {...props}
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <div className={styles.arrow}></div>
        </div>
        {error && <div className={styles.errorMessage}>{error}</div>}
      </div>
    );
  }
);

Select.displayName = 'Select';
