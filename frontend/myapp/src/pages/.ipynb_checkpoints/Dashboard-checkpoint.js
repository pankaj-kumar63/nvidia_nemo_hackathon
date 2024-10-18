import React, { useEffect, useState } from 'react';
import '../pages/Dashboard.css'; 
import NavbarSection from '../components/Navbar';
import Container from 'react-bootstrap/esm/Container';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import topic_wise_img from '../graphs/topic_wise_breakdown.png'
import overall_score_img from '../graphs/overall_score_distribution.png'
import chapter_wise_img from '../graphs/chapter_wise_analysis.png'
import student_progress_img from '../graphs/student_progress.png'
import neet_biology_exam_img from '../graphs/NEET_Biology_Exam_Accuracy_Over_Time.png'
import progress_compare_img from '../graphs/progress_compare.png'
function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      const token = sessionStorage.getItem('token'); // Get the token from session storage
      const user = sessionStorage.getItem('user'); // Get the user data from session storage
      const email = user ? JSON.parse(user).email : ''; // Extract email from user data
      const flag = 0;
      if (!token) {
        setError('User not logged in.');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('http://127.0.0.1:8993/api/dashboard/', {
          params: { email, flag },
        });
        console.log(response.data);
        setUserData(response.data); // Assuming the response has user data
      } catch (err) {
        setError('Failed to fetch user data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  // Render specific data from the userData object (e.g., userData.Response)
// Assuming your component structure remains the same
return (
  <div>
    <NavbarSection />
    <Container className="dashboard-body">
      <div className="tab-container">
        <Tabs defaultActiveKey="home" id="fill-tab-example" className="mb-3" fill>
          <Tab eventKey="home" title="Insights">
            <div className = "graphs text-center">
            <img src = {topic_wise_img} style = {{width:'40vw', height:'auto'}} alt = "topic-wise-graph"/>
            <img src = {chapter_wise_img} style = {{width:'40vw', height:'auto'}} alt = "chapter-wise-graph"/>
            <img src = {overall_score_img} style = {{width:'40vw', height:'auto'}} alt = "topic-wise-graph"/>
            <img src = {progress_compare_img} style = {{width:'40vw', height:'auto'}} alt = "progress-compare-graph"/>
            </div>
          </Tab>
          <Tab eventKey="profile" title="Report">
            <div className="markdown-report-data">
              <ReactMarkdown>{userData.Report}</ReactMarkdown>
            </div>
          </Tab>
          <Tab eventKey="longer-tab" title="Progress">
            <div className = "graphs text-center">
            <img src = {neet_biology_exam_img} style = {{width:'auto', height:'80vh'}} alt = "quiz-wise-graph"/>
            </div>
          </Tab>
        </Tabs>
      </div>
    </Container>
  </div>
);

}

export default Dashboard;
