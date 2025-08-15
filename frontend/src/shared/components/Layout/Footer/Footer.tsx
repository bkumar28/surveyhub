import React from 'react';
import styles from './Footer.module.scss';

interface FooterProps {
  collapsed?: boolean;
}

export const Footer: React.FC<FooterProps> = ({ collapsed = false }) => (
  <footer className={`${styles.footer} ${collapsed ? styles.collapsed : ''}`}>
    <div className={styles.copyright}>
      &copy; {new Date().getFullYear()} SurveyHub. All rights reserved.
    </div>

    <div className={styles.links}>
      <a href="/privacy" className={styles.link}>
        Privacy Policy
      </a>
      <a href="/terms" className={styles.link}>
        Terms of Service
      </a>
      <a href="/support" className={styles.link}>
        Support
      </a>
    </div>
  </footer>
);
