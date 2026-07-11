import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import MovieGrid from '../components/MovieGrid';

const Recommendations = () => {
  const [recs, setRecs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/recommend/collaborative').then(res => setRecs(res.data)).catch(console.error);
  }, []);

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '40px' }}>
      <div style={{ marginBottom: '40px', maxWidth: '800px', margin: '0 auto 40px auto' }}>
        <input 
          type="text" 
          placeholder="🔍 Search for movies..." 
          onClick={() => navigate('/search')}
          style={{ width: '100%', padding: '15px 20px', fontSize: '1.2rem', borderRadius: '30px', background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', color: 'var(--text-primary)', cursor: 'text', boxShadow: '0 4px 15px rgba(0,0,0,0.3)' }}
          readOnly
        />
      </div>
      <h1>AI Top Picks For You</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>Based on your ratings and watch history.</p>
      <MovieGrid movies={recs} />
    </div>
  );
};
export default Recommendations;
