import React, { useState, useEffect } from 'react';
import './Timer.css';

const Timer = () => {
    const [minutes, setMinutes] = useState(30);
    const [seconds, setSeconds] = useState(0);
    const [isActive, setIsActive] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [inputValue, setInputValue] = useState('00:00');

    useEffect(() => {
        let intervalId;
        setIsActive(true);
        if (isActive && !isPaused && (minutes > 0 || seconds > 0)) {
            intervalId = setInterval(() => {
                if (seconds > 0) {
                    setSeconds(seconds - 1);
                } else if (seconds === 0) {
                    if (minutes > 0) {
                        setMinutes(minutes - 1);
                        setSeconds(59);
                    }
                }
            }, 1000);
        }

        return () => clearInterval(intervalId);
    }, [isActive, isPaused, minutes, seconds]);

    const handleStart = () => {
        if (minutes === 0 && seconds === 0) {
            alert('Please set a valid time before starting.');
        } else {
            setIsActive(true);
            setIsPaused(false);
        }
    };

    const handlePause = () => {
        setIsPaused(!isPaused);
    };

    const handleReset = () => {
        setIsActive(false);
        setMinutes(0);
        setSeconds(0);
        setInputValue('00:00');
        setIsPaused(false);
    };

    const handleTimeClick = () => {
        setIsEditing(true);
    };

    const handleInputChange = (e) => {
        const value = e.target.value;
        setInputValue(value);
    };

    const handleInputBlur = () => {
        validateAndSetTime();
    };

    const handleInputKeyPress = (e) => {
        if (e.key === 'Enter') {
            validateAndSetTime(true); // Pass true to start the timer on Enter
        }
    };

    const validateAndSetTime = (shouldStartTimer = false) => {
        const timeParts = inputValue.split(':');
        if (timeParts.length === 2) {
            const newMinutes = parseInt(timeParts[0], 10);
            const newSeconds = parseInt(timeParts[1], 10);

            if (!isNaN(newMinutes) && !isNaN(newSeconds) && newSeconds >= 0 && newSeconds < 60) {
                setMinutes(newMinutes);
                setSeconds(newSeconds);
                setInputValue(`${newMinutes < 10 ? `0${newMinutes}` : newMinutes}:${newSeconds < 10 ? `0${newSeconds}` : newSeconds}`);
                setIsEditing(false);
                if (shouldStartTimer) {
                    handleStart();
                }
            } else {
                alert('Invalid time format. Please enter time in MM:SS format.');
            }
        } else {
            alert('Invalid time format. Please enter time in MM:SS format.');
        }
    };

    return (
        <div className='timer-component'>
            <div>
                {!isEditing ? (
                    <h2 onClick={handleTimeClick} style={{ cursor: 'pointer' }}>
                        {minutes < 10 ? `0${minutes}` : minutes}:{seconds < 10 ? `0${seconds}` : seconds}
                    </h2>
                ) : (
                    <input
                        type="text"
                        value={inputValue}
                        onChange={handleInputChange}
                        onBlur={handleInputBlur}
                        onKeyUp={handleInputKeyPress}
                        maxLength="5"
                        style={{ fontSize: '2em', textAlign: 'center' }}
                        autoFocus
                    />
                )}
            </div>
            <div>
                {/* {!isActive && <button onClick={handleStart}>Start</button>}
                {isActive && <button onClick={handlePause}>{isPaused ? 'Resume' : 'Pause'}</button>}
                <button onClick={handleReset}>Reset</button> */}
            </div>
        </div>
    );
};

export default Timer;
