import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import '../assets/css/app.css'; // Import your main theme CSS
import '../assets/vendor/css/bootstrap.min.css'; // Import Bootstrap if used

const ResetPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const history = useHistory();

  const handleResetPassword = async (e) => {
    e.preventDefault();
    // Here you would typically call an API to handle the password reset
    // For demonstration, we'll just simulate a successful response
    setMessage('If an account with that email exists, a reset link will be sent.');
    setTimeout(() => {
      history.push('/auth/login'); // Redirect to login after a delay
    }, 3000);
  };

  return (
    <div className="container">
      <h2 className="mt-5">Reset Password</h2>
      {message && <div className="alert alert-info">{message}</div>}
      <form onSubmit={handleResetPassword} className="mt-4">
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email address</label>
          <input
            type="email"
            className="form-control"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Send Reset Link</button>
      </form>
    </div>
  );
};

export default ResetPassword;
