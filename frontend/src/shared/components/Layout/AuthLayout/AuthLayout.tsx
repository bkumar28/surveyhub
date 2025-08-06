import React from 'react';
import styles from './AuthLayout.module.scss';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className={styles.layout}>
      <div className={styles.container}>
        <div className={styles.content}>
          <div className={styles.header}>
            <h1 className={styles.logo}>SurveyHub</h1>
            <p className={styles.tagline}>Create, distribute, and analyze surveys</p>
          </div>
          <div className={styles.formContainer}>
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};
