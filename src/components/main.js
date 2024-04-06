import React, { useState } from 'react';
import './App.css';
import { Link } from "react-router-dom";

const Main = () => {
    const [inputValue, setInputValue] = useState('');

    const handleInputChange = (event) => {
      setInputValue(event.target.value);
    };

    return (
        <div>
            <h1 className="title">Temporary Name</h1>
            <input
                className="inputBox"
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Enter a class name!"
            />
            <Link
                className='link-main-page'
                to="/result">
                Search
            </Link>
        </div>
    );
};
 
export default Main;