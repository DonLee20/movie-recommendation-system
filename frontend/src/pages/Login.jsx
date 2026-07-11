import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/recommendations');
    } catch (err) {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="container flex items-center justify-center animate-slide-up" style={{ minHeight: '60vh' }}>
      <form onSubmit={handleSubmit} className="glass" style={{ padding: '40px', borderRadius: '12px', width: '100%', maxWidth: '400px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h2 className="text-center glow-text">Login</h2>
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button type="submit" className="btn-primary">Login</button>
      </form>
    </div>
  );
};
export default Login;
