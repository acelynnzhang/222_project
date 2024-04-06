import React from "react";
import './App.css';
import { Link } from "react-router-dom";
import Card from './card.js';

const Results = () => {
    const cardsData = [
        {
          id: 1,
          title: 'Professor 1',
          description: 'This is the description for Card 1.',
          linkTo: '/card/1',
        },
        {
          id: 2,
          title: 'Professor 2',
          description: 'This is the description for Card 2.',
          linkTo: '/card/2',
        },
      ];

    return (
        <div>
            <h1 className="title">MAIN PAGE</h1>

            <div className="cards-container">
            {cardsData.map((card) => (
                <Card
                key={card.id}
                title={card.title}
                description={card.description}
                imageUrl={card.imageUrl}
                linkTo={card.linkTo}
                />
            ))}
            </div>
        </div>
    );
};
 
export default Results;