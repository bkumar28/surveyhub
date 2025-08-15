import React from 'react';
import { Card } from '../../../../shared/components/UI/Card';
import styles from './StatsCard.module.scss';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon?: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon,
  trend,
}) => {
  return (
    <Card className={styles.card}>
      <div className={styles.header}>
        <div className={styles.info}>
          <p className={styles.title}>{title}</p>
          <h3 className={styles.value}>{value}</h3>
        </div>
        {icon && <div className={styles.icon}>{icon}</div>}
      </div>
      {trend && (
        <div className={styles.trend}>
          <span className={`${styles.trendValue} ${trend.isPositive ? styles.positive : styles.negative}`}>
            {trend.isPositive ? '+' : ''}{trend.value}%
          </span>
          <span className={styles.trendLabel}>from last month</span>
        </div>
      )}
    </Card>
  );
};
