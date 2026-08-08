import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import AttackManager from './components/AttackManager'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
  }

  return (
    <Router>
      <div className="app">
        <header className="header">
          <h1>🔐 CyberResilience RL v14</h1>
          {token && <button onClick={handleLogout} className="logout-btn">Logout</button>}
        </header>
        <Routes>
          <Route path="/login" element={!token ? <Login onLogin={handleLogin} apiBase={API_BASE} /> : <Navigate to="/" />} />
          <Route path="/" element={token ? <Dashboard token={token} apiBase={API_BASE} /> : <Navigate to="/login" />} />
          <Route path="/attacks" element={token ? <AttackManager token={token} apiBase={API_BASE} /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
