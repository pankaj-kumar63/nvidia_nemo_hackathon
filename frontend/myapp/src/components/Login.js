import React, { useState } from 'react';
import axios from 'axios';
import './Login.css'; // Optional: You can create custom styling
import Container from 'react-bootstrap/esm/Container';
import NavbarSection from './Navbar';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from React Router

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate(); // Initialize useNavigate

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setErrorMessage('');

        try {
            const response = await axios.post('http://127.0.0.1:8993/api/login/', {
                email,
                password,
            });

            // If login is successful, save token and user info in sessionStorage
            const { token, user } = response.data;
            console.log('Token received:', token); // Debugging: Check if token is received
            sessionStorage.setItem('token', token.trim());
            sessionStorage.setItem('user', JSON.stringify(user));
            console.log('Token stored:', sessionStorage.getItem('token'));
            console.log('Login successful:', response.data);
            alert('Login successful!');

            // Redirect to home page after successful login
            navigate('/');  // Change '/home' to your home route

        } catch (error) {
            setErrorMessage('Invalid login credentials. Please try again.');
            console.error('Login failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Container className='login-body' fluid >
            <NavbarSection />
            <div className="login-container">
                <h2>Login</h2>
                <form onSubmit={handleSubmit} className="login-form" method='POST'>
                    <div className="form-group">
                        <div className='label'>Email:</div>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            placeholder="Enter your email"
                        />
                    </div>
                    <div className="form-group">
                        <div className='label'>Password:</div>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder="Enter your password"
                        />
                    </div>
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Logging in...' : 'Login'}
                    </button>
                    <div className = "text-center"><a href="/signup">New User ?</a></div>
                </form>
            </div>
        </Container>
    );
};

export default Login;
