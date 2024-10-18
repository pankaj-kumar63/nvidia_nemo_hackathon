import React from 'react'
import Button from 'react-bootstrap/esm/Button'
import Container from 'react-bootstrap/esm/Container'
import './MainPageText.css'
const MainPageText = () => {
    return (
        <Container className='main-div'>
            <div className='main-page-text'>
                <p>Welcome to AIcademy</p>
                <h1>Best Online Platform for NEET preparation</h1>
                <p>Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts.</p>
            </div>
            <div className='main-page-button'>
                <Button variant="primary">Get Started</Button>
                <Button variant="outline-primary">Learn More</Button>
            </div>
        </Container>
    )
}

export default MainPageText