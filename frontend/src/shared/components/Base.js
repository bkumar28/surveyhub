import React from 'react';
import '../assets/css/app.css'; // Import your main theme CSS
import '../assets/vendor/css/bootstrap.min.css'; // Import Bootstrap if used

const Base = ({ children }) => (
  <div className="app-wrapper">
    {/* Header */}
    <header className="main-header">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="/">SurveyHub</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item"><a className="nav-link" href="/">Home</a></li>
              <li className="nav-item"><a className="nav-link" href="/surveys">Surveys</a></li>
              <li className="nav-item"><a className="nav-link" href="/dashboard">Dashboard</a></li>
              <li className="nav-item"><a className="nav-link" href="/account/profile">Profile</a></li>
              <li className="nav-item"><a className="nav-link" href="/auth/login">Login</a></li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    {/* Main Content */}
    <main className="main-content container py-4">
      {children}
    </main>

    {/* Footer */}
    <footer className="main-footer bg-dark text-white text-center py-3 mt-auto">
      <div className="container">
        <p>&copy; 2025 SurveyHub. All rights reserved.</p>
      </div>
    </footer>
  </div>
);

export default Base;
