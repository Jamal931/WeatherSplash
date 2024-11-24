from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for React

# Replace with your OpenWeatherMap API Key
api_key = "6fcb2f32a1b0412975c7c3c438554a06"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    # OpenWeatherMap API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': response.json().get('message', 'Unable to fetch weather')}), response.status_code

    data = response.json()
    # Extract relevant fields for the response
    processed_data = {
        'city': data['name'],
        'temperature': {
            'kelvin': data['main']['temp'],
            'celsius': data['main']['temp'] - 273.15,
            'fahrenheit': (data['main']['temp'] - 273.15) * 9/5 + 32
        },
        'description': data['weather'][0]['description'],
        'weather_id': data['weather'][0]['id']
    }
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True)
