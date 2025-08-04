import React from 'react';

const RecentActivity = () => {
  const activities = [
    { id: 1, action: 'Created a new survey', timestamp: '2025-01-01 10:00 AM' },
    { id: 2, action: 'Completed a survey', timestamp: '2025-01-02 11:30 AM' },
    { id: 3, action: 'Updated profile information', timestamp: '2025-01-03 1:15 PM' },
    { id: 4, action: 'Logged in', timestamp: '2025-01-04 9:00 AM' },
    { id: 5, action: 'Logged out', timestamp: '2025-01-04 5:00 PM' },
  ];

  return (
    <div className="recent-activity">
      <h2>Recent Activity</h2>
      <ul className="list-group">
        {activities.map(activity => (
          <li key={activity.id} className="list-group-item">
            <span>{activity.action}</span>
            <span className="float-end text-muted">{activity.timestamp}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecentActivity;
