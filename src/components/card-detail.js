import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Link, useLocation } from "react-router-dom";

const CardDetails = () => {
  const { id } = useParams(); 
  const [cardDetails, setCardDetails] = useState(null);
  const [responseData, setResponseData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const location = useLocation();
  const { state } = location;
  const { prof = '', number = '', course='', difficulty='',numRatings='', takeAgain } = state || {};

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.post('http://127.0.0.1:5000/prof', {//cs473
          course: course,
          number: number,
          name: prof,
        }, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        setResponseData(response.data.split("\n"));
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []); 

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', marginTop: '45vh', transform: 'translateY(-50%)' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold', color:'white' }}>Loading...</h1>
      </div>
    );
}

  return (
    <div>
    			<h1 className="title">{prof}</h1>
    		<div>
					<p className='card-text'>Difficulty: {difficulty}%</p>
					<p className='card-text'>Number of Ratings: {numRatings}</p>
					<p className='card-text'>Take Again: {takeAgain}%</p>
				</div>

      {responseData && (
        <div>
            {responseData.map((item, index) => (
              <p className='card-text' key={index}>{item}</p>
            ))}
        </div>
      )}
    </div>
  );
};

export default CardDetails;