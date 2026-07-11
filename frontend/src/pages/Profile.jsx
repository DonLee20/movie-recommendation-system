import React, { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

const Profile = () => {
  const { user } = useContext(AuthContext);

  if (!user) return <div className="container">Please login.</div>;

  return (
    <div className="container animate-slide-up" style={{ paddingTop: '40px' }}>
      <div className="glass" style={{ padding: '40px', borderRadius: '12px', maxWidth: '600px', margin: '0 auto' }}>
        <h2>User Profile</h2>
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Joined:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
      </div>
    </div>
  );
};
export default Profile;
