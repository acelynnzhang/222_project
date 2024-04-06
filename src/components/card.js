import React from 'react';
import { Link } from 'react-router-dom';

const Card = ({ title, description, imageUrl, linkTo }) => {
  return (
    <div className="card">
      <img src={imageUrl} alt={title} />
      <div className="card-content">
        <h2>{title}</h2>
        <p>{description}</p>
        <Link to={linkTo}>Learn more</Link>
      </div>
    </div>
  );
};

export default Card;