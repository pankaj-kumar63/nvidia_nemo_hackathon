import React, { useState, useEffect } from 'react';
import { LiaRobotSolid } from "react-icons/lia";
import { RxCross2 } from "react-icons/rx";
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import '../pages/ChatBot.css'; // Optional: for styling
import VideoCarousel from './VideoCarousel'

const Chatbot = ({ handleShow }) => {
  const [messages, setMessages] = useState([
    { text: 'Hello! How can I assist you today?', sender: 'bot' },
  ]);
  const [userInput, setUserInput] = useState('');
  const [botReply, setBotReply] = useState('');
  const [ytLinks, setYtLinks] = useState([]);
  const handleUserInputChange = (e) => {
    setUserInput(e.target.value);
  };

  useEffect(() => {
    const urls = botReply.match(/https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[\w-]+|https?:\/\/m\.youtube\.com\/watch\?v=[\w-]+/g);
    if (urls) {
      setYtLinks(urls);
      sessionStorage.setItem('links', JSON.stringify(urls));
    }
  }, [botReply]);

  const handleSendMessage = async () => {
    if (userInput.trim() === '') return;

    setMessages([...messages, { text: userInput, sender: 'user' }]);
    setUserInput('');

    const botResponse = await getBotResponse(userInput);
    if (botResponse) {
      setBotReply(botResponse);
    }
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: botResponse, sender: 'bot' },
    ]);
  };

  const getBotResponse = async (message) => {
    const sent_message = {
      userMessage: message,
      flag: 1
    };
    const response = await axios.post('http://127.0.0.1:8993/api/llm-chat/', sent_message);
    return response.data.reply;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSendMessage();
  };

  return (
      <div className = "parent-container">
      <div className="chatbot-container">
        <div className="chat-messages">
          <h3 className="chatbot-icon">Learn {<LiaRobotSolid />}</h3>
          <h3 className="hide-chatpage-icon"><RxCross2 onClick={handleShow} /></h3>
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={userInput}
            onChange={handleUserInputChange}
            onKeyUp={handleKeyPress}
            placeholder="Type your message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
