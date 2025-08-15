import React from 'react';
import { Link } from 'react-router-dom';
import styles from './AuthLayout.module.scss';

interface AuthLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  hideTitle?: boolean;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({
  children,
  title = "Welcome to SurveyHub",
  subtitle = "Create powerful surveys, gather valuable insights, and make data-driven decisions with our comprehensive survey platform designed for businesses and researchers.",
  hideTitle = false
}) => {
  // Clone children and pass hideHeader prop to form components
  const childrenWithProps = React.Children.map(children, child => {
    // Check if it's a valid React element
    if (React.isValidElement(child)) {
      // Pass hideHeader=true to child components to prevent duplicate headers
      return React.cloneElement(child, { hideHeader: true } as any);
    }
    return child;
  });

  return (
    <div className={styles.layout}>
      {/* Left content section - hidden on mobile */}
      <section className={styles.contentSection}>
        <div className={styles.brandWrapper}>
          <Link to="/" className={styles.brand}>
            <span className={styles.brandPrimary}>Survey</span>
            <span className={styles.brandAccent}>Hub</span>
          </Link>
        </div>

        <div className={styles.contentBody}>
          {!hideTitle && (
            <>
              <h1 className={styles.contentTitle}>{title}</h1>
              <p className={styles.contentDescription}>
                {subtitle}
              </p>
            </>
          )}
          <div className={styles.features}>
            {/* Features content... */}
          </div>
        </div>

        <footer className={styles.contentFooter}>
          <p>© {new Date().getFullYear()} SurveyHub. All rights reserved.</p>
        </footer>
      </section>

      {/* Right form section */}
      <main className={styles.formSection}>
        {/* Mobile brand - only visible on smaller screens */}
        <div className={styles.mobileBrandWrapper}>
          <Link to="/" className={styles.mobileBrand}>
            <span className={styles.brandPrimary}>Survey</span>
            <span className={styles.brandAccent}>Hub</span>
          </Link>
        </div>

        <div className={styles.formContainer}>
          {/* Use the children with hideHeader prop */}
          {childrenWithProps}
        </div>
      </main>
    </div>
  );
};
