import React, { useEffect, useState } from 'react';
import api from '../services/api';
import MovieGrid from '../components/MovieGrid';

const Home = () => {
  const [trending, setTrending] = useState([]);
  const [topRated, setTopRated] = useState([]);

  useEffect(() => {
    api.get('/recommend/trending').then(res => setTrending(res.data)).catch(console.error);
    api.get('/recommend/top-rated').then(res => setTopRated(res.data)).catch(console.error);
  }, []);

  return (
    <div className="container animate-fade-in">
      <div style={{ padding: '60px 0', textAlign: 'center' }}>
        <h1 className="glow-text" style={{ fontSize: '3rem', marginBottom: '20px' }}>Welcome to MovieVerse</h1>
        <p style={{ fontSize: '1.2rem', color: 'var(--text-secondary)' }}>Discover your next favorite movie with AI.</p>
      </div>
      <h2>Trending Now</h2>
      <MovieGrid movies={trending} />
      <h2 style={{ marginTop: '40px' }}>Top Rated</h2>
      <MovieGrid movies={topRated} />
    </div>
  );
};
export default Home;
