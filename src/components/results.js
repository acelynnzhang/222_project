import React, { useState, useEffect } from "react";
import "./App.css";
import { Link, useLocation } from "react-router-dom";
import Card from "./card.js";
import axios from "axios";
const Results = () => {
	const [isLoading, setIsLoading] = useState(true);
	const [professorsData, setProfessorsData] = useState([]);
	const location = useLocation();
	const { state } = location;
	const { name = "", number = "" } = state || {};

	const isValidProfessorName = (name) => {
		return name.includes(",");
	};
      
	useEffect(() => {
        const fetchData = async () => {
            try {
              const response = await fetch(`http://127.0.0.1:5000/courselookup?course=${name}&number=${number}`);
              const data = await response.json();
              setProfessorsData(data);
              setIsLoading(false);
            } catch (error) {
              console.error('Error fetching data:', error);
              setIsLoading(false);
            }
          };
          fetchData();
	}, []);

	const combinedProfessorsData = professorsData.reduce((acc, curr) => {
		Object.entries(curr).forEach(([profName, courses]) => {
			if (isValidProfessorName(profName)) {
				if (!acc[profName]) {
					acc[profName] = { courses: [], info: {} };
				}
				if (Array.isArray(courses)) {
					acc[profName].courses = acc[profName].courses.concat(courses);
				} else {
					acc[profName].info = { ...acc[profName].info, ...courses };
				}
			}
		});
		return acc;
	}, {});

    if (isLoading) {
        return (
          <div style={{ textAlign: 'center', marginTop: '45vh', transform: 'translateY(-50%)' }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', color:'white' }}>Loading...</h1>
          </div>
        );
    }

	return (
		<div>
			<h1 className="title">CourseComparator</h1>
			<div>
				{Object.entries(combinedProfessorsData).map(([profName, data]) => (
					<Card
                        className='cards'
						// key={idx}
						title={profName}
						number={number}
						name={name}
						difficulty={(data.info.attendance_mandatory * 100).toFixed(2)}
						numRatings={data.info.num_ratings}
						takeAgain={(data.info.take_again * 100).toFixed(2)}
					/>
				))}
			</div>
		</div>
	);
};

export default Results;
