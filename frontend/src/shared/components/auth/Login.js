import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { login } from '../../services/auth'; // Import the login function from auth service
import Base from '../Base'; // Import the Base component for layout

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await login(email, password); // Call the login function
      history.push('/dashboard'); // Redirect to dashboard on successful login
    } catch (err) {
      setError('Invalid email or password'); // Set error message on failure
    }
  };

  return (
    <Base>
      <div className="container">
        <h2 className="text-center">Login</h2>
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email</label>
            <input
              type="email"
              className="form-control"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">Login</button>
        </form>
        <p className="mt-3">
          Don't have an account? <a href="/auth/register">Register here</a>
        </p>
      </div>
    </Base>
  );
};

export default Login;
