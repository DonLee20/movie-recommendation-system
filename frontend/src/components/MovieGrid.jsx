import React from 'react';
import MovieCard from './MovieCard';

const MovieGrid = ({ movies }) => (
  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px', padding: '20px 0' }}>
    {movies.map(movie => <MovieCard key={movie.movieId} movie={movie} />)}
  </div>
);
export default MovieGrid;
