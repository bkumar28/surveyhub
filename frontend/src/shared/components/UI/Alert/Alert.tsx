import React, { useState, useEffect } from 'react';
import styles from './Alert.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faInfoCircle,
  faCheckCircle,
  faExclamationTriangle,
  faExclamationCircle,
  faTimes
} from '@fortawesome/free-solid-svg-icons';

interface AlertProps {
  variant: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info';
  children: React.ReactNode;
  title?: string;
  dismissible?: boolean;
  onDismiss?: () => void;
  autoClose?: boolean | number;
  className?: string;
  icon?: boolean;
  testId?: string;
}

export const Alert: React.FC<AlertProps> = ({
  variant,
  children,
  title,
  dismissible = false,
  onDismiss,
  autoClose = false,
  className = '',
  icon = true,
  testId,
}) => {
  const [visible, setVisible] = useState(true);

  // Handle auto-close
  useEffect(() => {
    if (autoClose !== false && visible) {
      const timeout = setTimeout(() => {
        handleDismiss();
      }, typeof autoClose === 'number' ? autoClose : 5000);

      return () => clearTimeout(timeout);
    }
  }, [autoClose, visible]);

  const handleDismiss = () => {
    setVisible(false);
    if (onDismiss) onDismiss();
  };

  if (!visible) {
    return null;
  }

  // Get the appropriate icon based on variant
  const getIcon = () => {
    switch (variant) {
      case 'info':
      case 'primary':
        return faInfoCircle;
      case 'success':
        return faCheckCircle;
      case 'warning':
        return faExclamationTriangle;
      case 'danger':
        return faExclamationCircle;
      default:
        return faInfoCircle;
    }
  };

  return (
    <div
      className={`
        ${styles.alert}
        ${styles[`alert-${variant}`]}
        ${dismissible ? styles.dismissible : ''}
        ${className}
      `}
      role="alert"
      data-testid={testId}
    >
      <div className={styles.alertContent}>
        {icon && (
          <div className={styles.alertIcon}>
            <FontAwesomeIcon icon={getIcon()} />
          </div>
        )}

        <div className={styles.alertBody}>
          {title && <h4 className={styles.alertTitle}>{title}</h4>}
          <div className={styles.alertText}>{children}</div>
        </div>

        {dismissible && (
          <button
            type="button"
            className={styles.closeButton}
            onClick={handleDismiss}
            aria-label="Close"
            data-testid={testId ? `${testId}-close` : 'alert-close'}
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        )}
      </div>
    </div>
  );
};
