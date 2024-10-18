import React, { useEffect, useState } from 'react';
import "./Profile.css";
import NavbarSection from '../components/Navbar';
import Container from 'react-bootstrap/esm/Container';
import axios from 'axios';

function Profile() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      const token = sessionStorage.getItem('token'); // Get the token from session storage
      const user = sessionStorage.getItem('user'); // Get the user data from session storage
      const email = user ? JSON.parse(user).email : ''; // Extract email from user data
      if (!token) {
        setError('User not logged in.');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('http://127.0.0.1:8993/api/user/', {
          params: { email },
        });
        console.log(response.data)
        setUserData(response.data); // Assuming the response has user data
      } catch (err) {
        setError('Failed to fetch user data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <Container className='profile-body' fluid>
      <NavbarSection />
      <div className="profile">
        <h2>My Profile</h2>
        <form>
          <div className="row">
            <div className="profile-form-group">
              <label>First Name</label>
              <input
                type="text"
                name="firstName"
                value={userData.first_name || 'N/A'} // Use fetched user data
                disabled
              />
            </div>

            <div className="profile-form-group">
              <label>Second Name</label>
              <input
                type="text"
                name="secondName"
                value={userData.second_name || 'N/A'} // Use fetched user data
                disabled
              />
            </div>
          </div>

          <div className="row">
            <div className="profile-form-group">
              <label>Mobile</label>
              <input
                type="tel"
                name="mobile"
                value={userData.mobile || '00'} // Use fetched user data
                disabled
              />
            </div>

            <div className="profile-form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={userData.email || '00'} // Use fetched user data
                disabled
              />
            </div>
          </div>

          <div className="row">
            <div className="profile-form-group">
              <label>Chemistry</label>
              <input
                type="number"
                name="chemistry"
                value={userData.chemistry || '00'} // Use fetched user data
                disabled
              />
            </div>

            <div className="profile-form-group">
              <label>Biology</label>
              <input
                type="number"
                name="biology"
                value={userData.biology || '00'} // Use fetched user data
                disabled
              />
            </div>
          </div>

          <button disabled>Edit</button>
        </form>
      </div>
    </Container>
  );
}

export default Profile;
