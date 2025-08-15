import React from 'react';
import styles from './ThemeToggle.module.scss';
// Import your icons

interface ThemeToggleProps {
  // Avoid className if this is placed inside a button
  className?: string;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ className }) => {
  const [isDarkMode, setIsDarkMode] = React.useState(
    document.body.classList.contains('dark-theme')
  );

  const toggleTheme = () => {
    document.body.classList.toggle('dark-theme');
    setIsDarkMode(!isDarkMode);
    // Save preference to localStorage if needed
    localStorage.setItem('theme', isDarkMode ? 'light' : 'dark');
  };

  return (
    // Use a div when inside a button, or use button when standalone
    <div
      className={`${styles.toggleButton} ${className || ''}`}
      onClick={toggleTheme}
      role="button"
      tabIndex={0}
      aria-label={`Switch to ${isDarkMode ? 'light' : 'dark'} theme`}
    >
      {isDarkMode ? (
        <span className={styles.icon}>🌞</span> // Sun icon for light mode
      ) : (
        <span className={styles.icon}>🌙</span> // Moon icon for dark mode
      )}
    </div>
  );
};

export default ThemeToggle;
