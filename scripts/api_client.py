import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude, longitude):

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "wind_gusts_10m"
        ),
        "timezone": "auto"
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=parameters,
        timeout=10
    )

    response.raise_for_status()

    return response.json()