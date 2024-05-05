import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Card = ({ name, number, title, difficulty, numRatings, takeAgain }) => {
	const navigate = useNavigate();

	const handleSearch = () => {
		const data = {
			prof: title,
			course: name,
			number: number,
			difficulty:difficulty,
			numRatings:numRatings,
      takeAgain: takeAgain
		};
		navigate("/card", { state: data });
	};

	return (
		<div className="card">
			<div className="card-content">
				<h2>{title}</h2>
				<div>
					<p>Difficulty: {difficulty}%</p>
					<p>Number of Ratings: {numRatings}</p>
					<p>Take Again: {takeAgain}%</p>
				</div>
				<button className="learn-button" onClick={handleSearch}>Learn More</button>
			</div>
		</div>
	);
};

export default Card;
