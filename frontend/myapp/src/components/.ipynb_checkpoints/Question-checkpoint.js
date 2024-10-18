import React from 'react';
import './Question.css';

const Question = ({ question, userAnswer, handleAnswerSelect }) => {
    return (
        <div>
            <h3 className='question'>{question._id} {question.text}</h3>
            {question.options.map((option, index) => (
                <div key={index} className='option'>
                    <label>
                        <input
                            type="radio"
                            name={question._id}
                            value={index + 1} // Assigning option number (1-based index)
                            checked={userAnswer === (index + 1)} // Checking if user selected this option number
                            onChange={() => handleAnswerSelect(question._id, index + 1)} // Store option number
                        />
                        {option} {/* Display option text */}
                    </label>
                </div>
            ))}
        </div>
    );
};

export default Question;
