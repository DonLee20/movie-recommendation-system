import React, { useState, useEffect, useContext } from 'react';
import api from '../services/api';
import MovieGrid from '../components/MovieGrid';
import { AuthContext } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const { user, loading } = useContext(AuthContext);
  
  useEffect(() => {
    if (!user) return;
    const delayDebounceFn = setTimeout(() => {
      if (query.length > 2) {
        api.get(`/movies/search?query=${query}`).then(res => setResults(res.data)).catch(console.error);
      } else {
        setResults([]);
      }
    }, 500);
    return () => clearTimeout(delayDebounceFn);
  }, [query, user]);

  if (loading) return null;
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="container animate-slide-up" style={{ paddingTop: '40px' }}>
      <input 
        type="text" 
        placeholder="Search for movies..." 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        style={{ width: '100%', fontSize: '1.2rem', padding: '15px' }} 
      />
      <div style={{ marginTop: '20px' }}>
        {results.length > 0 ? <MovieGrid movies={results} /> : <p>Start typing to search...</p>}
      </div>
    </div>
  );
};
export default Search;
