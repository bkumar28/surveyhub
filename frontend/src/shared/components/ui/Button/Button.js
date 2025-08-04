import React from 'react';
import './Button.module.scss';

const Button = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  type = 'button',
  ...props
}) => {
  const baseClass = 'btn';
  const classes = `${baseClass} ${baseClass}--${variant} ${baseClass}--${size}`;

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
