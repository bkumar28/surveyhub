import React from 'react';
import { NavLink } from 'react-router-dom';
import styles from './Sidebar.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChartBar,
  faClipboardList,
  faUsers,
  faChartLine,
  faCog,
  faChevronLeft,
  faChevronRight,
  faQuestion,
  faBook
} from '@fortawesome/free-solid-svg-icons';

interface SidebarProps {
  isOpen: boolean;
  onToggle?: () => void;
}

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: faChartBar },
  { path: '/surveys', label: 'Surveys', icon: faClipboardList },
  { path: '/users', label: 'Users', icon: faUsers },
  { path: '/analytics', label: 'Analytics', icon: faChartLine },
  { path: '/settings', label: 'Settings', icon: faCog },
];

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle }) => (
  <aside className={`${styles.sidebar} ${!isOpen ? styles.collapsed : ''}`}>
    <div className={styles.brand}>
      {isOpen ? (
        <span className={styles.brandText}>
          <span className={styles.brandPrimary}>Survey</span>
          <span className={styles.brandAccent}>Hub</span>
        </span>
      ) : (
        <span className={styles.brandShort}>SH</span>
      )}
    </div>

    <nav className={styles.nav}>
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            `${styles.navItem} ${isActive ? styles.active : ''}`
          }
        >
          <span className={styles.icon}>
            <FontAwesomeIcon icon={item.icon} />
          </span>
          {isOpen && <span className={styles.label}>{item.label}</span>}
          {!isOpen && (
            <div className={styles.tooltip}>{item.label}</div>
          )}
        </NavLink>
      ))}

    </nav>

  </aside>
);
