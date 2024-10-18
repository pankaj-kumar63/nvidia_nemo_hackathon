import React, { useEffect, useState } from 'react';
import Question from '../components/Question';
import Result from '../components/Result';
import Button from 'react-bootstrap/esm/Button';
import axios from 'axios';
import Timer from '../components/Timer';
import Container from 'react-bootstrap/esm/Container';

const Test = () => {
  const [userAnswers, setUserAnswers] = useState({});
  const [showResult, setShowResult] = useState(false);
  const [questions, setQuestions] = useState([]);
  const user = sessionStorage.getItem('user');
  const email = user ? JSON.parse(user).email : '';

  // Save user answers to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('userAnswers', JSON.stringify(userAnswers));
  }, [userAnswers]);

  // Retrieve saved answers from localStorage on component mount
  useEffect(() => {
    const savedAnswers = localStorage.getItem('userAnswers');
    if (savedAnswers) {
      setUserAnswers(JSON.parse(savedAnswers));
    }

    const fetchQuestions = async () => {
      try {
        const { data } = await axios.get('http://127.0.0.1:8993/api/questions/');
        console.log("Fetched questions:", data);
        if (Array.isArray(data)) {
          setQuestions(data);
        } else {
          console.error("Fetched data is not an array:", data);
        }
      } catch (error) {
        console.error("Error fetching questions:", error);
      }
    };

    fetchQuestions();
  }, []);

  const handleAnswerSelect = (questionId, answer) => {
    setUserAnswers({ ...userAnswers, [questionId]: answer });
  };

const handleSubmit = async () => {
  setShowResult(true);

  // Calculate the score in the frontend
  const calculateScore = () => {
    let score = 0;
    questions.forEach((question) => {
      if (userAnswers[question._id] === question.correct_option) {
        score += 1;
      }
    });
    return score;
  };

  const score = calculateScore();  // Store the calculated score

  // Log the questions, user answers, and score in console
  console.log("Questions submitted:", questions);
  console.log("User answers submitted:", userAnswers);
  console.log("Score submitted:", score);

  // Optionally, clear localStorage on submit
  localStorage.removeItem('userAnswers');

  try {
    // Make a POST request to save the answers and score via Django API
    const response = await axios.post('http://127.0.0.1:8993/api/save-answers/', {
      email: email,
      answers: userAnswers,  // Send user answers
      questions: questions,  // Send the questions as well
      score: score,          // Send the calculated score
      timestamp: new Date().toISOString(),  // Include a timestamp
    });

    console.log("Answers and score successfully saved:", response.data);
  } catch (error) {
    console.error("Error saving answers and score:", error);
  }
};


  return (
    <Container>
      {!showResult ? (
        <div>
          <div className='test-timer'><Timer /></div>
          <h1 className="text-center">Test</h1>
          {questions.length > 0 ? (
            questions.map((question) => (
              <Question
                key={question._id}
                question={question}
                userAnswer={userAnswers[question._id]}
                handleAnswerSelect={handleAnswerSelect}
              />
            ))
          ) : (
            <p>Loading questions...</p>
          )}
          <br />
          <Button onClick={handleSubmit}>Submit</Button>
        </div>
      ) : (
        <Result questions={questions} userAnswers={userAnswers} />
      )}
    </Container>
  );
};

export default Test;
