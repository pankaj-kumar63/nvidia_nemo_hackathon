import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null); // Initially null to indicate loading

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    
    // Debug: Log the token and authentication status
    console.log('Token in ProtectedRoute:', token);
    
    // Check if token exists and set authentication status
    if (token && token.trim() !== '') {
      setIsAuthenticated(true); // Set authenticated if token is valid
    } else {
      setIsAuthenticated(false); // Redirect if no token
    }
  }, []); // Runs once when the component mounts

  // Loading state while determining authentication status
  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Show loading until check is done
  }

  return isAuthenticated ? children : <Navigate to="/login" />; // Redirect if not authenticated
};

export default ProtectedRoute;
