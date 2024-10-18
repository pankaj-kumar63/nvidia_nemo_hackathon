import React, { useState } from 'react';
import './Signup.css';
import NavbarSection from './Navbar';
import Container from 'react-bootstrap/esm/Container';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from React Router

function SignupForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    secondName: '',
    mobile: '',
    email: '',
    password: '',
    className: '',
  });
  const navigate = useNavigate(); // Initialize useNavigate

  // Handling input change to update state
  const handleChange = (e) => {
    setFormData({
      ...formData, // Keep existing form data
      [e.target.name]: e.target.value, // Update only the field being changed
    });
  };

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Student Data:', formData);

    // Send form data to Django API
    axios.post('http://127.0.0.1:8993/api/save-student/', formData)
      .then((response) => {
        console.log('Student created:', response.data);
        alert('Student created successfully!');
        
        // Redirect to home page after successful signup
        navigate('/login');  // Change '/home' to your home route
      })
      .catch((error) => {
        console.error('Student creation failed:', error);
        alert('Failed to create student. Please try again.');
      });
  };

  return (
    <Container className='signup-body' fluid ><NavbarSection/>
    <div className="SignupForm">
      <h2>Student Signup</h2>
      <form onSubmit={handleSubmit} method='POST'>
        <div className="row">
          <div className="form-group">
            <label>First Name:</label>
            <input
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Second Name:</label>
            <input
              type="text"
              name="secondName"
              value={formData.secondName}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="row">
          <div className="form-group">
            <label>Mobile Number:</label>
            <input
              type="tel"
              name="mobile"
              value={formData.mobile}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="row">
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Class:</label>
            <input
              type="text"
              name="className"
              value={formData.className}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <button type="submit">Sign Up</button>
      </form>
    </div>
    </Container>
  );
}

export default SignupForm;
