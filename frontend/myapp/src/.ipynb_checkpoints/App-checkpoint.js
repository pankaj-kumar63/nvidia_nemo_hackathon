import './App.css';
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import MainPage from './pages/MainPage';
import Test from './pages/Test';
import ChatBot from './pages/ChatBot';
import Login from './components/Login';
import SignupForm from './components/Signup';
import ProtectedRoute from './components/ProtectedRoute'; // Import ProtectedRoute
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';

function App() {
  return (
    <>
      <BrowserRouter>
        <div className="App">
          <Routes>
            <Route path="/" element={<MainPage />} />
            
            {/* Public Routes */}
            <Route path='/login' element={<Login />} />
            <Route path='/signup' element={<SignupForm />} />

            {/* Protected Routes */}
            <Route path='/test' element={
              <ProtectedRoute>
                <Test />
              </ProtectedRoute>
            } />
            <Route path='/chatbot' element={
              <ProtectedRoute>
                <ChatBot />
              </ProtectedRoute>
            } />
            <Route path='/profile' element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } />
            <Route path='/dashboard' element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      </BrowserRouter>
    </>
  );
}

export default App;
