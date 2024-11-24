import React, { useState } from 'react';
import axios from 'axios';

const Weather = () => {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState(null);

  const getWeather = () => {
    axios
      .get(`/weather?city=${city}`)
      .then((response) => {
        setWeather(response.data);
        setError(null);
      })
      .catch((err) => {
        setError('City not found or API error');
        setWeather(null);
      });
  };

  return (
    <div>
      <h1>Weather Forecast</h1>
      <input
        type="text"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="Enter city"
      />
      <button onClick={getWeather}>Get Weather</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {weather && (
        <div>
          <h3>Weather in {weather.city}</h3>
          <p>Temperature: {weather.temperature.celsius.toFixed(2)}°C</p>
          <p>{weather.description}</p>
        </div>
      )}
    </div>
  );
};

export default Weather;
