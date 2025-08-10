import React, { useState, useRef, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../../../app/store';
import { logout } from '../../../../features/auth/authSlice';
import styles from './Header.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faBell, faUser, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { NavLink } from 'react-router-dom';

interface HeaderProps {
  onMenuClick: () => void;
  sidebarOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick, sidebarOpen }) => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const handleLogout = () => {
    dispatch(logout());
  };

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className={`${styles.header} ${!sidebarOpen ? styles.collapsed : ''}`}>
      <div className={styles.left}>
        <button
          className={styles.menuButton}
          onClick={onMenuClick}
          aria-label={sidebarOpen ? 'Close menu' : 'Open menu'}
        >
          <FontAwesomeIcon icon={faBars} size="lg" />
        </button>
      </div>
      <div className={styles.right}>
        <button className={styles.iconButton} aria-label="Notifications">
          <FontAwesomeIcon icon={faBell} size="lg" />
        </button>
        {user && (
          <div className={styles.userMenu} ref={menuRef}>
            <button
              className={`${styles.userButton} ${menuOpen ? styles.active : ''}`}
              onClick={() => setMenuOpen((open) => !open)}
              aria-label="User menu"
            >
              <div className={styles.avatar}>
                {user.firstName ? user.firstName.charAt(0) : 'U'}
              </div>
              <span className={styles.userName}>
                {user.firstName} {user.lastName}
              </span>
            </button>
            {/* Use the show class instead of conditional rendering */}
            <div className={`${styles.dropdown} ${menuOpen ? styles.show : ''}`}>
              <NavLink to="/profile" className={styles.dropdownItem}>
                <span className={styles.dropdownIcon}>
                  <FontAwesomeIcon icon={faUser} />
                </span>
                Profile
              </NavLink>
              <NavLink to="/settings" className={styles.dropdownItem}>
                <span className={styles.dropdownIcon}>
                  <FontAwesomeIcon icon={faCog} />
                </span>
                Settings
              </NavLink>
              <div className={styles.dropdownDivider}></div>
              <button
                className={`${styles.dropdownItem} ${styles.danger}`}
                onClick={handleLogout}
              >
                <span className={styles.dropdownIcon}>
                  <FontAwesomeIcon icon={faSignOutAlt} />
                </span>
                Logout
              </button>
            </div>

            {/* Add overlay to catch clicks outside */}
            {menuOpen && (
              <div
                className={`${styles.overlay} ${styles.show}`}
                onClick={() => setMenuOpen(false)}
              />
            )}
          </div>
        )}
      </div>
    </header>
  );
};
