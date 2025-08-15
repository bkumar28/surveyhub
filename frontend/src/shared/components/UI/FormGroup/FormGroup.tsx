import React from 'react';
import styles from './FormGroup.module.scss';

interface FormGroupProps {
  children: React.ReactNode;
  label?: string;
  required?: boolean;
  helpText?: string;
  className?: string;
}

export const FormGroup: React.FC<FormGroupProps> = ({
  children,
  label,
  required = false,
  helpText,
  className = '',
}) => {
  return (
    <div className={`${styles.formGroup} ${className}`}>
      {label && (
        <label className={styles.label}>
          {label}
          {required && <span className={styles.requiredMark}>*</span>}
        </label>
      )}
      <div className={styles.inputContainer}>{children}</div>
      {helpText && <div className={styles.helpText}>{helpText}</div>}
    </div>
  );
};
