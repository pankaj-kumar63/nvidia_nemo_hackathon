import React from 'react'
import { AiFillSafetyCertificate } from "react-icons/ai";
import { FaBookReader } from "react-icons/fa";
import './SuccessSection.css'
const SuccessSection = () => {
    return (
        <div>
            <div className='success-section d-flex'>
                <div className='all-cards d-flex'>
                    <div className='success-section-icon'>
                        <FaBookReader />
                    </div>
                    <div className='success-section-content'>
                        <h3>Success</h3>
                        <p>Your message has been sent successfully</p>
                    </div>
                </div>
                <div className='all-cards d-flex'>
                    <div className='success-section-icon'>
                        <FaBookReader />
                    </div>
                    <div className='success-section-content'>
                        <h3>Success</h3>
                        <p>Your message has been sent successfully</p>
                    </div>
                </div>
                <div className='all-cards d-flex'>
                    <div className='success-section-icon'>
                        <FaBookReader />
                    </div>
                    <div className='success-section-content'>
                        <h3>Success</h3>
                        <p>Your message has been sent successfully</p>
                    </div>
                </div>
                <div className='all-cards d-flex '>
                    <div className='success-section-icon '>
                        <FaBookReader />
                    </div>
                    <div className='success-section-content '>
                        <h3>Success</h3>
                        <p>Your message has been sent successfully</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SuccessSection