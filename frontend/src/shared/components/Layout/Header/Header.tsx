import React from 'react';
import { useAppDispatch, useAppSelector } from '../../../../app/store';
import { logout } from '../../../../features/auth/authSlice';
import { Button } from '../../UI/Button';
import styles from './Header.module.scss';

interface HeaderProps {
  onMenuClick: () => void;
  sidebarOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick, sidebarOpen }) => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <button
          className={styles.menuButton}
          onClick={onMenuClick}
          aria-label={sidebarOpen ? 'Close menu' : 'Open menu'}
        >
          <span className={styles.menuIcon}></span>
        </button>
        <h1 className={styles.logo}>SurveyHub</h1>
      </div>

      <div className={styles.right}>
        {user && (
          <div className={styles.userMenu}>
            <span className={styles.userName}>
              {user.firstName} {user.lastName}
            </span>
            <Button variant="outline" size="sm" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        )}
      </div>
    </header>
  );
};
