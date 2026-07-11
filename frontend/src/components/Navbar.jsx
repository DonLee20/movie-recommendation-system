import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="glass" style={{ padding: '15px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'sticky', top: 0, zIndex: 100 }}>
      <Link to="/" style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>🎬 MovieVerse</Link>
      <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
        {user ? (
          <>
            <Link to="/recommendations">For You</Link>
            <Link to="/watchlist">Watchlist</Link>
            <Link to="/profile">Profile</Link>
            <button onClick={handleLogout} className="btn-primary" style={{ background: 'transparent', border: '1px solid var(--accent-color)' }}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn-primary" style={{ background: 'transparent', border: '1px solid var(--accent-color)' }}>Login</Link>
            <Link to="/signup" className="btn-primary">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
};
export default Navbar;
