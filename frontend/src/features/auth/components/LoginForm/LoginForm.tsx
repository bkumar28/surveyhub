import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../../../app/store';
import { login, clearError } from '../../authSlice';
import { Button } from '../../../../shared/components/UI/Button';
import { Input } from '../../../../shared/components/UI/Input';
import styles from './LoginForm.module.scss';

export const LoginForm: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember: false,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { loading, error, isAuthenticated } = useAppSelector((state) => state.auth);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    return () => {
      dispatch(clearError());
    };
  }, [dispatch]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    dispatch(login(formData));
  };

  return (
    <div className={styles.formContainer}>
      <div className={styles.header}>
        <span style={{
          display: 'inline-block',
          fontWeight: 700,
          fontSize: '2rem',
          marginBottom: '1rem',
          letterSpacing: '0.05em'
        }}>
          <span style={{ color: 'var(--color-primary-dark)' }}>Survey</span>
          <span style={{ color: 'var(--color-accent)', marginLeft: 2 }}>Hub</span>
        </span>
        <h1>Sign In</h1>
      </div>
      <form className={styles.form} onSubmit={handleSubmit}>
        {error && <div className={styles.errorAlert}>{error}</div>}
        <div className={styles.inputGroup}>
          <Input
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            placeholder="Enter your email"
            required
          />
        </div>
        <div className={styles.inputGroup}>
          <Input
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            placeholder="Enter your password"
            required
          />
        </div>
        <div className={styles.rememberRow}>
          <label style={{ display: 'flex', alignItems: 'center', fontSize: '0.95rem', cursor: 'pointer', marginBottom: 0 }}>
            <input
              type="checkbox"
              name="remember"
              checked={formData.remember}
              onChange={handleChange}
              style={{ marginRight: '0.5rem' }}
            />
            Remember me
          </label>
          <a href="#" className={styles.link}>Forgot password?</a>
        </div>
        <Button
          type="submit"
          loading={loading}
          fullWidth
          size="lg"
          className={styles.btn}
        >
          Sign In
        </Button>
        <div className={styles.footer}>
          <button type="button" onClick={() => navigate('/register')} className={styles.link}>
            Sign up
          </button>
        </div>
      </form>
    </div>
  );
};
