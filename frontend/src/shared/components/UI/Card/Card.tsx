import React from 'react';
import styles from './Card.module.scss';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
  shadow?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  padding = 'md',
  shadow = true,
}) => {
  const classes = [
    styles.card,
    styles[padding],
    shadow && styles.shadow,
    className,
  ].filter(Boolean).join(' ');

  return <div className={classes}>{children}</div>;
};
