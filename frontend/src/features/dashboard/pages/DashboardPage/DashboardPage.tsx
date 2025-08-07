import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../../../app/store';
import { fetchDashboardStats } from '../../dashboardSlice';
import { StatsCard } from '../../components/StatsCard';
import styles from './DashboardPage.module.scss';

export const DashboardPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { stats, loading, error } = useAppSelector((state) => state.dashboard);

  useEffect(() => {
    dispatch(fetchDashboardStats());
  }, [dispatch]);

  if (loading) {
    return <div className={styles.loading}>Loading dashboard...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error: {error}</div>;
  }

  return (
    <div className={styles.dashboard}>
      <div className={styles.header}>
        <h1>Dashboard</h1>
        <p>Welcome back! Here's what's happening with your surveys.</p>
      </div>

      <div className={styles.stats}>
        <StatsCard
          title="Total Surveys"
          value={stats?.totalSurveys || 0}
          icon="📊"
          trend={{ value: 12, isPositive: true }}
        />
        <StatsCard
          title="Total Responses"
          value={stats?.totalResponses || 0}
          icon="📝"
          trend={{ value: 8, isPositive: true }}
        />
        <StatsCard
          title="Active Users"
          value={stats?.activeUsers || 0}
          icon="👥"
          trend={{ value: 3, isPositive: false }}
        />
        <StatsCard
          title="Completion Rate"
          value={`${stats?.completionRate || 0}%`}
          icon="✅"
          trend={{ value: 5, isPositive: true }}
        />
      </div>

      <div className={styles.content}>
        <div className={styles.section}>
          <h2>Recent Activity</h2>
          <div className={styles.placeholder}>
            <p>Recent activity will be displayed here</p>
          </div>
        </div>

        <div className={styles.section}>
          <h2>Quick Actions</h2>
          <div className={styles.actions}>
            <button className={styles.actionButton}>Create New Survey</button>
            <button className={styles.actionButton}>View Analytics</button>
            <button className={styles.actionButton}>Manage Users</button>
          </div>
        </div>
      </div>
    </div>
  );
};
