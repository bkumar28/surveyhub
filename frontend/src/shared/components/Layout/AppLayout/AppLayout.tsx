import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../Header';
import { Sidebar } from '../Sidebar';
import styles from './AppLayout.module.scss';

export const AppLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className={styles.layout}>
      <Header
        onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        sidebarOpen={sidebarOpen}
      />
      <div className={styles.container}>
        <Sidebar isOpen={sidebarOpen} />
        <main className={`${styles.main} ${!sidebarOpen ? styles.expanded : ''}`}>
          <Outlet />
        </main>
      </div>
    </div>
  );
};
