import React from 'react';
import styles from './ProgressBar.module.scss';

interface ProgressBarProps {
  progress: number;
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info';
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  labelPosition?: 'inside' | 'outside';
  className?: string;
  striped?: boolean;
  animated?: boolean;
  customLabel?: string;
  testId?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  variant = 'primary',
  size = 'md',
  showLabel = false,
  labelPosition = 'inside',
  className = '',
  striped = false,
  animated = false,
  customLabel,
  testId,
}) => {
  // Ensure progress is within 0-100 range
  const safeProgress = Math.min(Math.max(progress, 0), 100);

  // Format progress for display
  const formattedProgress = Math.round(safeProgress);
  const label = customLabel || `${formattedProgress}%`;

  return (
    <div
      className={`${styles.progressContainer} ${className}`}
      data-testid={testId}
    >
      <div
        className={`
          ${styles.progress}
          ${styles[`progress-${size}`]}
        `}
        role="progressbar"
        aria-valuenow={formattedProgress}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={`
            ${styles.progressBar}
            ${styles[`progress-${variant}`]}
            ${striped ? styles.striped : ''}
            ${animated ? styles.animated : ''}
          `}
          style={{ width: `${safeProgress}%` }}
        >
          {showLabel && labelPosition === 'inside' && (
            <span className={styles.progressLabel}>{label}</span>
          )}
        </div>
      </div>

      {showLabel && labelPosition === 'outside' && (
        <span className={styles.progressLabelOutside}>{label}</span>
      )}
    </div>
  );
};
