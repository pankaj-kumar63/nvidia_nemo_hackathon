import Image from 'react-bootstrap/Image';
import './SecondSection.css';
import Container from 'react-bootstrap/esm/Container';
import Row from 'react-bootstrap/esm/Row';
import Col from 'react-bootstrap/esm/Col';
import img from '../static/woman-smiling.jpg';
import { FaBookReader } from "react-icons/fa";
import { FaPersonRays } from "react-icons/fa6";
import { LiaCertificateSolid } from "react-icons/lia";
function SecondSection() {
    return (
        <>
            <Container style={{ paddingLeft: '0px', paddingRight: '0px' }} fluid>
                <Row >
                    <Col>
                        <Image src={img} style={{ height: '100vh', width: 'auto', display:'block', margin:'auto' }} />
                    </Col>
                    <Col>
                        <div className='right-card'>
                            <p style={{marginTop:'25px'}}>CRACK NEET </p>
                            <h2>Benefits About Online Learning Expertise</h2>
                            <div className="second-section-cards card mt-3">
                                <div className="card-body d-flex">
                                    <div className = "card-icon"><FaBookReader/></div>
                                    <div className='ms-2'>
                                    <h5 className="card-title">Special title treatment</h5>
                                    <p className="card-text">With supporting text below as a natural lead-in to additional content.</p>
                                    </div>
                                </div>
                            </div>
                            <div className="card mt-3">
                                <div className="card-body d-flex">
                                <div className = "card-icon"><LiaCertificateSolid/></div>
                                    <div className='ms-2'>
                                    <h5 className="card-title">Special title treatment</h5>
                                    <p className="card-text">With supporting text below as a natural lead-in to additional content.</p>
                                    </div>
                                </div>
                            </div>
                            <div className="card mt-3">
                                <div className="card-body d-flex">
                                <div className = "card-icon"><FaPersonRays/></div>
                                    <div className='ms-2'>
                                    <h5 className="card-title">Special title treatment</h5>
                                    <p className="card-text">With supporting text below as a natural lead-in to additional content.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Col>
                </Row>
            </Container>
        </>
    )
}

export default SecondSection;