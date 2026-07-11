import React, { useEffect, useState } from 'react';
import api from '../services/api';
import MovieGrid from '../components/MovieGrid';

const Favorites = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    api.get('/favorites').then(res => setMovies(res.data)).catch(console.error);
  }, []);

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '40px' }}>
      <h1>Your Favorites</h1>
      {movies.length > 0 ? <MovieGrid movies={movies} /> : <p>No favorites yet.</p>}
    </div>
  );
};
export default Favorites;
