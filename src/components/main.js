import React, { useState } from "react";
import "./App.css";
import { Link } from "react-router-dom";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Main = () => {
	const [courseName, setCourseName] = useState("");
	const [courseNumber, setCourseNumber] = useState("");
	const navigate = useNavigate();

	const handleCourseNameChange = (event) => {
		setCourseName(event.target.value);
	};

	const handleCourseNumberChange = (event) => {
		setCourseNumber(event.target.value);
	};

	const handleSearch = () => {
		const data = { name: courseName, number: courseNumber };
		navigate("/result", { state: data });
	};

	return (
		<div>
			<h1 className="title">CourseComparator</h1>
			<div className="inputContainer">
				<input
					className="inputBox"
					type="text"
					value={courseName}
					onChange={handleCourseNameChange}
					placeholder="Course Name"
				/>
				<input
					className="inputBox"
					type="text"
					value={courseNumber}
					onChange={handleCourseNumberChange}
					placeholder="Course Number"
				/>
			</div>
			<button className="search-button" onClick={handleSearch}>Search</button>
		</div>
	);
};

export default Main;
