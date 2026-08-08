import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

function Dashboard({ token, apiBase }) {
  const [stats, setStats] = useState({ status: 'Online', mode: 'Real', version: '14.0.0' })
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchStats() }, [])

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${apiBase}/health`)
      setStats({ ...stats, ...res.data })
    } catch (e) {}
    setLoading(false)
  }

  return (
    <div className="container">
      <nav className="nav">
        <Link to="/" className="active">Dashboard</Link>
        <Link to="/attacks">Attack Manager</Link>
      </nav>

      <div className="grid">
        <div className="card metric">
          <div className="metric-value" style={{color:'#22c55e'}}>●</div>
          <div className="metric-label">System Status: {stats.status}</div>
        </div>
        <div className="card metric">
          <div className="metric-value">{stats.mode || 'Real'}</div>
          <div className="metric-label">Mode</div>
        </div>
        <div className="card metric">
          <div className="metric-value">{stats.version || '14.0.0'}</div>
          <div className="metric-label">Version</div>
        </div>
        <div className="card metric">
          <div className="metric-value">9</div>
          <div className="metric-label">Active Tools</div>
        </div>
      </div>

      <div className="card">
        <h2>🚀 Quick Start</h2>
        <p style={{color:'#94a3b8', marginBottom:'16px'}}>
          This is the REAL tool execution dashboard. Training is done locally via Docker.
        </p>
        <code>
          docker build -t cyber-rl .<br/>
          docker run -it --network=host \\<br/>
          &nbsp;&nbsp;python use_tool.py --target http://host.docker.internal:3000 \\<br/>
          &nbsp;&nbsp;--train --episodes 2000 --explicit-auth
        </code>
      </div>
    </div>
  )
}

export default Dashboard
