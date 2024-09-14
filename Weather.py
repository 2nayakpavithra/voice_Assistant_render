import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
dotenv_path = 'C:/Users/dell/Desktop/Voice_assistant/apid.env'
if not load_dotenv(dotenv_path):
    print("Failed to load environment variables.")

# Fetch API key from the environment variables
weather_api_key = os.getenv('Weather_api_key')


def get_weather(city):
    api_address = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(api_address)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data: {response.status_code}")
        print(f"Response content: {response.text}")
        return None


def temp(city):
    json_data = get_weather(city)
    if json_data:
        temperature = round(json_data['main']['temp'] - 273.15, 1)  # Convert from Kelvin to Celsius
        return temperature
    else:
        return None


def des(city):
    json_data = get_weather(city)
    if json_data:
        description = json_data['weather'][0]['description']
        return description
    else:
        return None

