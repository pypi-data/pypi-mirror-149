# ~/dev/weather/__init__.py

# Here we import both our client modules
from weather import weather_client, geolocation_client

# This takes a string as input and returns a tuple of floats
# (latituted, longitude)
# Since it is only used internally and not for public purpose
# we prepend it with an underscore (_) to make it explicit
def _get_latitude_and_longitude(city: str) -> (float, float):
    # Here we get the decoded JSON response
    response = geolocation_client.get_geolocation_information(city)

    # We cast the 'latt' and 'longt' values into floats and
    # returns them in a tuple
    return (float(response["latt"]), float(response["longt"]))

    # parentheses are here optional. This would work too
    # return float(response["latt"]), float(response["longt"])


# This takes a city string as parameter and will return
# a float (the temperature in celsius)
def get_current_temperature(city: str) -> float:
    # Here we unpack the tuple to directly get both values
    latitude, longitude = _get_latitude_and_longitude(city)
    # This is equivalent to
    # coordinates = _get_latitude_and_logitude(city)
    # latitude = coordinates[0]
    # longitude = coordinates[1]

    # Here we get the decoded JSON response
    response = weather_client.get_current_weather(latitude, longitude)

    # We directly return the value from the JSON since
    # it is already a float
    return response["current_weather"]["temperature"]
