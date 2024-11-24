// src/Weather.js
import React from 'react';

const Weather = ({ temperature, description }) => {
  return (
    <div>
      <h3>Temperature: {temperature}°C</h3>
      <p>{description}</p>
    </div>
  );
}

export default Weather;
