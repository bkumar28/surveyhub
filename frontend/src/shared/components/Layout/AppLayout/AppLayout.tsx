import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../Header/Header';
import { Sidebar } from '../Sidebar/Sidebar';
import { Footer } from '../Footer/Footer';
import styles from './AppLayout.module.scss';

export const AppLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className={styles.layout}>
      <Sidebar isOpen={sidebarOpen} />
      <div className={`${styles.mainArea} ${!sidebarOpen ? styles.collapsed : ''}`}>
        <Header
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          sidebarOpen={sidebarOpen}
        />
        <main className={styles.mainContent}>
          <Outlet />
        </main>
        <Footer collapsed={!sidebarOpen} />
      </div>
    </div>
  );
};
