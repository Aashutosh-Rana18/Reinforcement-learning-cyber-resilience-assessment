import React, { useState } from 'react'
import axios from 'axios'

function Login({ onLogin, apiBase }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [otp, setOtp] = useState('')
  const [userId, setUserId] = useState('')
  const [step, setStep] = useState('login')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleRegister = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      await axios.post(`${apiBase}/api/auth/register`, { email, password })
      setError('Registered! Now login.')
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed')
    }
    setLoading(false)
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      const res = await axios.post(`${apiBase}/api/auth/login`, { email, password })
      setUserId(res.data.user_id)
      setStep('otp')
      setError(`OTP sent: ${res.data.otp}`)
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed')
    }
    setLoading(false)
  }

  const handleVerifyOtp = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      const res = await axios.post(`${apiBase}/api/auth/verify-otp`, { user_id: userId, otp })
      onLogin(res.data.token)
    } catch (err) {
      setError(err.response?.data?.error || 'OTP verification failed')
    }
    setLoading(false)
  }

  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '80px' }}>
      <div className="card">
        <h2>🔐 {step === 'login' ? 'Login' : 'Verify OTP'}</h2>
        {step === 'login' ? (
          <form onSubmit={handleLogin}>
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Sending OTP...' : 'Login'}
            </button>
            <button type="button" className="btn" onClick={handleRegister} disabled={loading} style={{background:'#3b82f6'}}>
              Register
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyOtp}>
            <input type="text" placeholder="Enter OTP" value={otp} onChange={e => setOtp(e.target.value)} required />
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
            <button type="button" className="btn" onClick={() => setStep('login')} style={{background:'#64748b'}}>
              Back
            </button>
          </form>
        )}
        {error && <p className={error.includes('sent') || error.includes('Registered') ? 'success' : 'error'}>{error}</p>}
      </div>
    </div>
  )
}

export default Login
