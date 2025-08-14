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
      <button className={styles.menuToggle} onClick={onMenuClick}>
        <div className="hamburger align-self-center">
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
        </div>
      </button>

      <div className={styles.headerContent}>
        <div className={styles.searchContainer}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="Search..."
          />
          <i className={`fas fa-search ${styles.searchIcon}`}></i>
        </div>
      </div>

      <div className={styles.headerRight}>
        {/* Notifications dropdown */}
        <div className={styles.dropdown} ref={notificationsRef}>
          <button
            className={styles.dropdownToggle}
            onClick={() => {
              setNotificationsOpen(!notificationsOpen);
              setUserDropdownOpen(false);
            }}
          >
            <i className="fas fa-bell"></i>
          </button>
          <div className={`${styles.dropdownMenu} ${notificationsOpen ? styles.show : ''}`}>
            <div className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-envelope"></i></span>
              <span>New message received</span>
            </div>
            <div className={styles.dropdownDivider}></div>
            <div className={styles.dropdownItem}>
              <span className={styles.icon}><i className="fas fa-chart-line"></i></span>
              <span>Survey results updated</span>
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
          >
            <img src="/assets/images/avatars/avatar.svg" alt="User" />
            <div className={styles.userInfo}>
              <span className={styles.userName}>John Doe</span>
              <span className={styles.userRole}>Administrator</span>
            </div>
            <i className="fas fa-chevron-down"></i>
          </button>
          <div className={`${styles.dropdownMenu} ${userDropdownOpen ? styles.show : ''}`}>
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
