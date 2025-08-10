import React from 'react';
import styles from './Footer.module.scss';

interface FooterProps {
  collapsed?: boolean;
}

export const Footer: React.FC<FooterProps> = ({ collapsed = false }) => (
  <footer className={`${styles.footer} ${collapsed ? styles.collapsed : ''}`}>
    &copy; {new Date().getFullYear()} SurveyHub. All rights reserved.
  </footer>
);
