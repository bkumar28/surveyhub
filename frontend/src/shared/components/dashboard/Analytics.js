import React from 'react';
import { Line } from 'react-chartjs-2';

const Analytics = () => {
  const data = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'User Engagement',
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="analytics-container">
      <h2 className="text-center">User Engagement Analytics</h2>
      <Line data={data} options={options} />
    </div>
  );
};

export default Analytics;
