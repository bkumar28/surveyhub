import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AppRouter } from './app/router';
import { ErrorBoundary } from './shared/components/feedback';

function App() {
  return (
    <div className="App">
      <ErrorBoundary>
        <AppRouter />
      </ErrorBoundary>
    </div>
  );
}

export default App;
