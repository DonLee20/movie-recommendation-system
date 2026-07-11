import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signup } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup(username, email, password);
      navigate('/login');
    } catch (err) {
      alert('Signup failed. Username or email might be taken.');
    }
  };

  return (
    <div className="container flex items-center justify-center animate-slide-up" style={{ minHeight: '60vh' }}>
      <form onSubmit={handleSubmit} className="glass" style={{ padding: '40px', borderRadius: '12px', width: '100%', maxWidth: '400px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h2 className="text-center glow-text">Sign Up</h2>
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button type="submit" className="btn-primary">Create Account</button>
      </form>
    </div>
  );
};
export default Signup;
