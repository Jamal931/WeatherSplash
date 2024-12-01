// src/Weather.js
import React from 'react';

const Weather = ({ temperature, description }) => {
  return (
    <div>
      <h3>Temperature: {temperature}°C</h3>
      <p>Weather temperature={25} description="Sunny with a gentle breeze"</p>
    </div>
  );
}

export default Weather;
