import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Search from './pages/Search';
import Movie from './pages/Movie';
import Recommendations from './pages/Recommendations';
import Favorites from './pages/Favorites';
import Watchlist from './pages/Watchlist';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Signup from './pages/Signup';
import NotFound from './pages/NotFound';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="flex flex-col" style={{ minHeight: '100vh' }}>
          <Navbar />
          <main style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/search" element={<Search />} />
              <Route path="/movie/:id" element={<Movie />} />
              <Route path="/recommendations" element={<Recommendations />} />
              <Route path="/favorites" element={<Favorites />} />
              <Route path="/watchlist" element={<Watchlist />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
