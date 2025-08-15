import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../Header/Header';
import { Sidebar } from '../Sidebar/Sidebar';
import { Footer } from '../Footer/Footer';
import styles from './AppLayout.module.scss';

export const AppLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className={styles.wrapper}>
      {/* Sidebar - fixed on the left */}
      <Sidebar isOpen={sidebarOpen} />

      {/* Main content container */}
      <div className={`${styles.mainWrapper} ${!sidebarOpen ? styles.sidebarCollapsed : ''}`}>
        {/* Header at the top of main area */}
        <Header
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          sidebarOpen={sidebarOpen}
        />

        {/* Main content that scrolls */}
        <main className={styles.contentWrapper}>
          <div className={styles.contentContainer}>
            <Outlet />
          </div>
        </main>

        {/* Footer at the bottom of main area */}
        <Footer collapsed={!sidebarOpen} />
      </div>
    </div>
  );
};
