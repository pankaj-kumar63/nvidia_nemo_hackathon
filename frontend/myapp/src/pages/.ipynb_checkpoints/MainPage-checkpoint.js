import React, { useState, useEffect } from 'react';
import NavbarSection from '../components/Navbar';
import './MainPage.css';
import SecondSection from './SecondSection';
import MainPageText from '../components/MainPageText';
import img from '../static/bg-img.jpg';
import SuccessSection from './SuccessSection';
import ChatBot from './ChatBot';
import Timer from '../components/Timer';
import VideoCarousel from './VideoCarousel'
const MainPage = () => {
  const [show, setShow] = useState(false);
  const storedLinks = sessionStorage.getItem('links');
  const links = storedLinks ? JSON.parse(storedLinks) : [];
  const handleShow = () => {
      setShow(!show);
      sessionStorage.setItem('show', JSON.stringify(true));
  }
  return (
    <div>
      <div className='main-page'>
        <img src={img} alt="main" />
        {/* <div>
        <Timer initialMinutes={1} initialSeconds={30} />
      </div> */}
        <NavbarSection handleShow={handleShow} />
        <MainPageText />
        <div className={`chatbot-wrapper ${show ? 'visible' : ''}`}>
          <ChatBot handleShow={handleShow}/>
        </div>
      </div>
      <div>
        <SecondSection />
      </div>
      <div>
        <SuccessSection />
      </div>
{show && links && <VideoCarousel videoUrls = {links}/>}
    </div>
  );
};

export default MainPage;
