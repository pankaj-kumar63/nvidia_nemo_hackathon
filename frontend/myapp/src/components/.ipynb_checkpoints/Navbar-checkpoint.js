import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './Navbar.css';
import { useNavigate } from 'react-router-dom'; // For navigation

function NavbarSection({ handleShow }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate(); // React Router's navigation hook

  // Check if the user is logged in by checking for the token in sessionStorage
  useEffect(() => {
    const token = sessionStorage.getItem('token');
    setIsLoggedIn(!!token); // Set to true if token exists, otherwise false
  }, []);

  // Handle the logout process
  const handleLogout = () => {
    sessionStorage.removeItem('token'); // Remove the token from sessionStorage
    setIsLoggedIn(false); // Update state to reflect logged-out status
    navigate('/login'); // Redirect to login page
  };

  return (
    <Navbar expand="lg" className="main-navbar mt-5">
      <Container>
        <Navbar.Toggle className="toggler" aria-controls="navbarScroll " />
        <Navbar.Collapse id="navbarScroll">
          <Nav className="me-auto my-2 my-lg-0 " style={{ maxHeight: 'auto' }} navbarScroll>
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/test">Test</Nav.Link>
            <Nav.Link href="/profile">Profile</Nav.Link>
            <Nav.Link href="/dashboard">Dashboard</Nav.Link>
                      {/* Conditionally render Login or Logout button next to the Ask button */}
          {isLoggedIn ? (
            <Nav.Link onClick = {handleLogout}>Logout</Nav.Link>
          ) : (
            <Nav.Link href="/login">Login</Nav.Link>
          )}
          </Nav>
        </Navbar.Collapse>
        <Form className="right-side-button d-flex">
          <Button onClick={handleShow} className="btn" variant="outline-success">
            Ask?
          </Button>
        </Form>
      </Container>
    </Navbar>
  );
}

export default NavbarSection;
