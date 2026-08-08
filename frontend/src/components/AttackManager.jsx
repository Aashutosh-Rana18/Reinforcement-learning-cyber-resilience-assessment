import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

function AttackManager({ token, apiBase }) {
  const [target, setTarget] = useState('http://host.docker.internal:3000')
  const [auth, setAuth] = useState(false)
  const [attacks, setAttacks] = useState([])
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const headers = { Authorization: `Bearer ${token}` }

  useEffect(() => { fetchAttacks() }, [])

  const fetchAttacks = async () => {
    try {
      const res = await axios.get(`${apiBase}/api/attacks?limit=10`, { headers })
      setAttacks(res.data.attacks || [])
    } catch (e) {}
  }

  const createAttack = async () => {
    if (!auth) { setMessage('You must confirm authorization!'); return }
    setLoading(true); setMessage('')
    try {
      const res = await axios.post(`${apiBase}/api/attacks`, {
        target_url: target, attack_mode: 'reconnaissance', aggression_level: 5
      }, { headers })
      setMessage(`Attack created: ${res.data.attack_id}`)
      fetchAttacks()
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed')
    }
    setLoading(false)
  }

  return (
    <div className="container">
      <nav className="nav">
        <Link to="/">Dashboard</Link>
        <Link to="/attacks" className="active">Attack Manager</Link>
      </nav>

      <div className="grid">
        <div className="card">
          <h2>▶ New Assessment</h2>
          <input type="text" value={target} onChange={e => setTarget(e.target.value)} placeholder="Target URL" />
          <label>
            <input type="checkbox" checked={auth} onChange={e => setAuth(e.target.checked)} />
            I have written authorization to test this target
          </label>
          <button className="btn" onClick={createAttack} disabled={loading}>
            {loading ? 'Creating...' : 'Start Assessment'}
          </button>
          {message && <p className={message.includes('created') ? 'success' : 'error'}>{message}</p>}
        </div>

        <div className="card">
          <h2>📋 Recent Assessments</h2>
          {attacks.length === 0 ? (
            <p style={{color:'#64748b'}}>No assessments yet</p>
          ) : (
            attacks.map(a => (
              <div key={a.id} style={{padding:'12px', borderBottom:'1px solid #334155', display:'flex', justifyContent:'space-between'}}>
                <span>{a.target_url}</span>
                <span style={{color: a.status === 'running' ? '#22c55e' : '#94a3b8'}}>{a.status}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default AttackManager
