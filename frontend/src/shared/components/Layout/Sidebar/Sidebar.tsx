import React from 'react';
import { NavLink } from 'react-router-dom';
import styles from './Sidebar.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChartBar,
  faClipboardList,
  faQuestionCircle,
  faChartLine,
  faCommentDots,
  faFileAlt,
  faBell,
  faTimes,
  faBars
} from '@fortawesome/free-solid-svg-icons';

interface SidebarProps {
  isOpen: boolean;
  onToggle?: () => void;
}

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: faChartBar },
  { path: '/surveys', label: 'Surveys', icon: faClipboardList },
  { path: '/questions', label: 'Questions', icon: faQuestionCircle },
  { path: '/responses', label: 'Responses', icon: faCommentDots },
  { path: '/templates', label: 'Templates', icon: faFileAlt },
  { path: '/notifications', label: 'Notifications', icon: faBell },
  { path: '/analytics', label: 'Analytics', icon: faChartLine },
];

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle }) => (
  <>
    {/* Mobile overlay */}
    {isOpen && (
      <div
        className={styles.mobileOverlay}
        onClick={onToggle}
      />
    )}

    <aside className={`${styles.sidebar} ${!isOpen ? styles.collapsed : ''} ${isOpen ? styles.expanded : ''}`}>
      <div className={styles.brand}>
        <div className={styles.brandContent}>
          {isOpen ? (
            <span className={styles.brandText}>
              <span className={styles.brandPrimary}>Survey</span>
              <span className={styles.brandAccent}>Hub</span>
            </span>
          ) : (
            <span className={styles.brandShort}>SH</span>
          )}
        </div>

      </div>

      <nav className={styles.nav}>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `${styles.navItem} ${isActive ? styles.active : ''}`
            }
            onClick={() => {
              // Close sidebar on mobile when navigating
              if (window.innerWidth <= 768 && onToggle) {
                onToggle();
              }
            }}
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

      <div className={styles.sidebarFooter}>
        <div className={styles.footerInfo}>
        </div>
      </div>
    </aside>
  </>
);
