import React from 'react';
import { Link } from 'react-router-dom';

const MovieCard = ({ movie }) => {
  return (
    <Link to={`/movie/${movie.movieId}`} className="card-hover glass" style={{ borderRadius: '12px', overflow: 'hidden', display: 'block' }}>
      <img src={movie.poster || 'https://via.placeholder.com/500x750?text=No+Poster'} alt={movie.title} style={{ width: '100%', height: '300px', objectFit: 'cover' }} />
      <div style={{ padding: '15px' }}>
        <h3 style={{ fontSize: '1.1rem', marginBottom: '5px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{movie.title}</h3>
        <p style={{ color: 'var(--accent-color)', fontSize: '0.9rem' }}>⭐ {movie.average_rating}</p>
      </div>
    </Link>
  );
};
export default MovieCard;
