import React, { useEffect, useState } from 'react';
import api from '../services/api';
import MovieGrid from '../components/MovieGrid';

const Watchlist = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    api.get('/watchlist').then(res => setMovies(res.data)).catch(console.error);
  }, []);

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '40px' }}>
      <h1>Your Watchlist</h1>
      {movies.length > 0 ? <MovieGrid movies={movies} /> : <p>Your watchlist is empty.</p>}
    </div>
  );
};
export default Watchlist;
