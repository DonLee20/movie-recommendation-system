import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Note: profile is in the user_data router but mounted directly on app?
          // Wait, in main.py we included user_data.router without prefix.
          const res = await api.get('/profile');
          setUser(res.data);
        } catch (err) {
          console.error('Error fetching profile', err);
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };
    fetchUser();
  }, []);

  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const res = await api.post('/auth/login', formData);
    localStorage.setItem('token', res.data.access_token);
    const profileRes = await api.get('/profile');
    setUser(profileRes.data);
  };

  const signup = async (username, email, password) => {
    await api.post('/auth/signup', { username, email, password });
    // User will be redirected to login page manually
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
