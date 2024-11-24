import sys
import time
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize UI components
        self.city_label = QLabel("Enter city name:")
        self.city_input = QLineEdit(self)
        self.unit_selector = QComboBox(self)  # Dropdown for selecting temperature unit
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.extra_info_label = QLabel(self)  # Label for humidity, wind, etc.
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Enhanced Weather App")
        self.setWindowIcon(QIcon("weather_icon.png"))  # Add your custom icon file

        # Set up the layout
        vbox = QVBoxLayout()
        
        # Add components
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        
        hbox_units = QHBoxLayout()  # Unit selector beside the button
        self.unit_selector.addItems(["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"])
        hbox_units.addWidget(self.unit_selector)
        hbox_units.addWidget(self.get_weather_button)
        vbox.addLayout(hbox_units)
        
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.extra_info_label)

        self.setLayout(vbox)

        # Center align all labels
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.extra_info_label.setAlignment(Qt.AlignCenter)

        # Apply style
        self.setStyleSheet("""
               QLabel, QPushButton, QComboBox {
                   font-family: Calibri;
               }
               QLabel#city_label {
                   font-size: 30px;
                   font-style: italic;
               }
               QLineEdit#city_input {
                   font-size: 20px;
                   padding: 5px;
               }
               QPushButton#get_weather_button {
                   font-size: 20px;
                   font-weight: bold;
               }
               QLabel#temperature_label {
                   font-size: 50px;
                   font-weight: bold;
               }
               QLabel#emoji_label {
                   font-size: 80px;
                   font-family: Apple Color emoji;
               }
               QLabel#extra_info_label {
                   font-size: 18px;
                   color: gray;
               }
        """)

        # Connect button click to the function
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        """Fetch weather data from OpenWeatherMap API."""
        api_key = "6fcb2f32a1b0412975c7c3c438554a06"  # Replace with your own API key
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Unknown error"))

        except requests.exceptions.HTTPError as http_err:
            self.display_error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error. Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out.")
        except requests.exceptions.RequestException as req_err:
            self.display_error(f"Request error: {req_err}")

    def display_weather(self, data):
        """Display weather information on the UI."""
        temperature_k = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        sunrise = time.strftime("%H:%M:%S", time.gmtime(data["sys"]["sunrise"]))
        sunset = time.strftime("%H:%M:%S", time.gmtime(data["sys"]["sunset"]))

        # Convert temperature based on selected unit
        unit = self.unit_selector.currentText()
        if unit == "Celsius (°C)":
            temperature = temperature_k - 273.15
            temperature_str = f"{temperature:.0f}°C"
        elif unit == "Fahrenheit (°F)":
            temperature = (temperature_k - 273.15) * 9 / 5 + 32
            temperature_str = f"{temperature:.0f}°F"
        else:  # Kelvin
            temperature_str = f"{temperature_k:.0f} K"

        # Update labels
        self.temperature_label.setText(temperature_str)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        self.extra_info_label.setText(
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Sunrise: {sunrise} EST\n"
            f"Sunset: {sunset} EST"
        )

    def display_error(self, message):
        """Show an error message to the user."""
        QMessageBox.warning(self, "Error", message)
        self.temperature_label.clear()
        self.emoji_label.clear()
        self.description_label.clear()
        self.extra_info_label.clear()

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌧️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🏙️"
        elif weather_id <= 804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
