# ~/dev/weather-project/weather/geolocation_client.py

import requests
from weather.exceptions import ApiError

API_URL = "https://geocode.xyz/{city}"


def get_geolocation_information(city: str):
    url = API_URL.format(city=city)

    params = {"json": True}
    response = requests.get(url, params=params)

    content = response.json()
    if response.status_code != 200 or "error" in content:
        raise ApiError(f"City not found")

    return content
