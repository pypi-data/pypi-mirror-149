# ~/dev/weather-project/weather/weather_client.py

import requests
from weather.exceptions import ApiError

API_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }
    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        raise ApiError(f"Error: {response.status_code}")

    return response.json()
