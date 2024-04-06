import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const CardDetails = () => {
  const { id } = useParams(); 
  const [cardDetails, setCardDetails] = useState(null);

  useEffect(() => {
    const fetchCardDetails = async () => {
      try {
        const response = await fetch(`https://api.example.com/cards/${id}`);
        const data = await response.json();
        setCardDetails(data);
      } catch (error) {
        console.error('Error fetching card details:', error);
      }
    };

    fetchCardDetails();
  }, [id]);

  if (!cardDetails) {
    return <div>Loading...</div>;
  }

  return (
    <div className="card-details">
      <h2>{cardDetails.title}</h2>
      <img src={cardDetails.imageUrl} alt={cardDetails.title} />
      <p>{cardDetails.description}</p>
      <p> info: {cardDetails.additionalInfo}</p>
    </div>
  );
};

export default CardDetails;