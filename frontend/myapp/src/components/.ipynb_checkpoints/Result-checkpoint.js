import React from 'react';
import './Result.css'; // Assuming you already have the styling in this file

const Result = ({ questions, userAnswers }) => {
  const calculateScore = () => {
    let score = 0;
    questions.forEach((question) => {
      if (userAnswers[question._id] === question.correct_option) {
        score += 1;
      }
    });
    return score;
  };

  // Function to get the actual text of the selected option
  const getAnswerText = (question, selectedOption) => {
    const optionIndex = selectedOption - 1; // Since options are 1-based, we need to subtract 1
    return question.options[optionIndex];   // Fetch the option text
  };

  return (
    <div className="result-container">
      <h2 className="result-title">Your Result</h2>
      <p className="result-score">
        You scored <strong>{calculateScore()}</strong> out of <strong>{questions.length}</strong>.
      </p>

      <ol className="result-list">
        {questions.map((question, index) => (
          <li key={index} className="result-item">
            <p className="question-text">
              <strong>{index + 1}. {question.text}</strong>
            </p>
            <p className="user-answer">
              <span>Your answer: </span>
              {userAnswers[question._id]
                ? <span className="highlight-user-answer">{getAnswerText(question, userAnswers[question._id])}</span>
                : <span className="not-answered">Not answered</span>}
            </p>
            <p className="correct-answer">
              <span>Correct answer: </span>
              <span className="highlight-correct-answer">{getAnswerText(question, question.correct_option)}</span>
            </p>
          </li>
        ))}
      </ol>
    </div>
  );
};

export default Result;
