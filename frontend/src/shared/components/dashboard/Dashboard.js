import React from 'react';
import Base from '../Base';
import Analytics from './Analytics';
import RecentActivity from './RecentActivity';

const Dashboard = () => {
  return (
    <Base>
      <div className="dashboard">
        <h1 className="dashboard-title">Dashboard</h1>
        <div className="dashboard-content">
          <Analytics />
          <RecentActivity />
        </div>
      </div>
    </Base>
  );
};

export default Dashboard;
