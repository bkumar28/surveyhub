import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.scss';

interface HeaderProps {
  onMenuClick: () => void;
  sidebarOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick, sidebarOpen }) => {
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const userDropdownRef = useRef<HTMLDivElement>(null);
  const notificationsRef = useRef<HTMLDivElement>(null);

  // Close dropdowns when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      // User dropdown
      if (userDropdownRef.current && !userDropdownRef.current.contains(event.target as Node)) {
        setUserDropdownOpen(false);
      }

      // Notifications dropdown
      if (notificationsRef.current && !notificationsRef.current.contains(event.target as Node)) {
        setNotificationsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <header className={styles.header}>
      <button className={styles.menuToggle} onClick={onMenuClick} aria-label="Toggle sidebar">
        <div className={styles.hamburger}>
          <span className={styles.hamburgerLine}></span>
          <span className={styles.hamburgerLine}></span>
          <span className={styles.hamburgerLine}></span>
        </div>
      </button>

      <div className={styles.headerRight}>
        {/* Notifications dropdown */}
        <div className={styles.dropdown} ref={notificationsRef}>
          <button
            className={styles.dropdownToggle}
            onClick={() => {
              setNotificationsOpen(!notificationsOpen);
              setUserDropdownOpen(false);
            }}
            aria-label="Notifications"
          >
            <i className="fas fa-bell"></i>
            <span className={styles.notificationBadge}></span>
          </button>
          <div className={`${styles.dropdownMenu} ${notificationsOpen ? styles.show : ''}`}>
            <div className={styles.dropdownHeader}>
              <span>Notifications</span>
            </div>
            <div className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-envelope"></i></span>
              <div className={styles.notificationContent}>
                <span className={styles.notificationTitle}>New message received</span>
                <span className={styles.notificationTime}>10 minutes ago</span>
              </div>
            </div>
            <div className={styles.dropdownDivider}></div>
            <div className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-chart-line"></i></span>
              <div className={styles.notificationContent}>
                <span className={styles.notificationTitle}>Survey results updated</span>
                <span className={styles.notificationTime}>1 hour ago</span>
              </div>
            </div>
            <div className={styles.dropdownFooter}>
              <Link to="/notifications">View all notifications</Link>
            </div>
          </div>
        </div>

        {/* User dropdown */}
        <div className={`${styles.dropdown} ${styles.userDropdown}`} ref={userDropdownRef}>
          <button
            className={styles.dropdownToggle}
            onClick={() => {
              setUserDropdownOpen(!userDropdownOpen);
              setNotificationsOpen(false);
            }}
            aria-label="User menu"
          >
            <img src="/assets/images/avatars/avatar.svg" alt="User" />
            <div className={styles.userInfo}>
              <span className={styles.userName}>John Doe</span>
              <span className={styles.userRole}>Administrator</span>
            </div>
            <i className={`fas fa-chevron-down ${styles.dropdownArrow} ${userDropdownOpen ? styles.rotate : ''}`}></i>
          </button>
          <div className={`${styles.dropdownMenu} ${userDropdownOpen ? styles.show : ''}`}>
            <div className={styles.dropdownHeader}>
              <span>Account</span>
            </div>
            <Link to="/profile" className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-user"></i></span>
              <span>Profile</span>
            </Link>
            <Link to="/settings" className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-cog"></i></span>
              <span>Settings</span>
            </Link>
            <div className={styles.dropdownDivider}></div>
            <Link to="/logout" className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-sign-out-alt"></i></span>
              <span>Sign out</span>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};
