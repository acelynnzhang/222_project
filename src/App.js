import React, { useState } from 'react';
import './App.css';
import './index.css';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  return (
    <div className="App"> 
      <h1 className="title">Temporary Name</h1>
      <input
        className="inputBox"
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter a class name!"
      />
    </div>
  );
}


export default App;
