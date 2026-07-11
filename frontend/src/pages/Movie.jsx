import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import MovieGrid from '../components/MovieGrid';

const Movie = () => {
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const [movie, setMovie] = useState(null);
  const [contentRecs, setContentRecs] = useState([]);
  const [hybridRecs, setHybridRecs] = useState([]);

  useEffect(() => {
    api.get(`/movies/${id}`).then(res => setMovie(res.data)).catch(console.error);
    api.get(`/recommend/content/${id}`).then(res => setContentRecs(res.data)).catch(console.error);
    if (user) {
      api.get(`/recommend/hybrid/${id}`).then(res => setHybridRecs(res.data)).catch(console.error);
    }
  }, [id, user]);

  const addToWatchlist = () => api.post('/watchlist', { movie_id: id }).then(() => alert('Added to watchlist'));
  const addToFavorites = () => api.post('/favorites', { movie_id: id }).then(() => alert('Added to favorites'));

  if (!movie) return <div className="container" style={{paddingTop: '40px'}}>Loading...</div>;

  return (
    <div className="animate-fade-in">
      {movie.backdrop && (
        <div style={{ width: '100%', height: '400px', backgroundImage: `url(${movie.backdrop})`, backgroundSize: 'cover', backgroundPosition: 'center', opacity: 0.5, position: 'absolute', top: 0, zIndex: -1 }}></div>
      )}
      <div className="container" style={{ display: 'flex', gap: '40px', paddingTop: '60px' }}>
        <img src={movie.poster} alt={movie.title} style={{ width: '300px', borderRadius: '12px' }} className="glass" />
        <div>
          <h1 style={{ fontSize: '2.5rem' }}>{movie.title}</h1>
          <p style={{ color: 'var(--accent-color)', fontSize: '1.2rem', marginBottom: '20px' }}>⭐ {movie.average_rating} | {movie.release_date}</p>
          <p style={{ fontSize: '1.1rem', marginBottom: '20px', lineHeight: '1.8' }}>{movie.overview}</p>
          <div style={{ display: 'flex', gap: '15px' }}>
            {user && (
              <>
                <button onClick={addToWatchlist} className="btn-primary">Add to Watchlist</button>
                <button onClick={addToFavorites} className="btn-primary" style={{ background: 'var(--card-bg)', border: '1px solid var(--accent-color)' }}>Favorite</button>
              </>
            )}
          </div>
        </div>
      </div>
      
      <div className="container" style={{ marginTop: '60px' }}>
        <h2>Similar Movies (Content Based)</h2>
        <MovieGrid movies={contentRecs} />
        
        {user && hybridRecs.length > 0 && (
          <div style={{ marginTop: '40px' }}>
            <h2>Recommended For You (AI Hybrid)</h2>
            <MovieGrid movies={hybridRecs} />
          </div>
        )}
      </div>
    </div>
  );
};
export default Movie;
