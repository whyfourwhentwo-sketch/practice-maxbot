import React from 'react';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Дашборд ЖКХ</h1>
          <p>Мониторинг проблем и обращений граждан</p>
        </div>
      </header>
      <Dashboard />
    </div>
  );
}

export default App;