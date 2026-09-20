import json
import socket
from urllib import error, request

from psx.utils.display import header, sep


def _has_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def _fetch_weather():
    if not _has_internet_connection():
        return None

    try:
        req = request.Request(
            "https://wttr.in/?format=j1",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with request.urlopen(req, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (error.URLError, ValueError, TimeoutError):
        return None

    current = payload.get("current_condition", [{}])[0]
    if not current:
        return None

    weather_desc = current.get("weatherDesc", [{"value": "Unknown"}])[0].get("value", "Unknown")
    temp_c = current.get("temp_C", "Unknown")
    feels_like = current.get("FeelsLikeC", "Unknown")
    location = payload.get("nearest_area", [{"areaName": [{"value": "Unknown"}]}])[0].get("areaName", [{"value": "Unknown"}])[0].get("value", "Unknown")

    return {
        "location": location,
        "weather": weather_desc,
        "temp_c": temp_c,
        "feels_like": feels_like,
    }


def run():
    length = header("Weather")
    weather = _fetch_weather()

    if weather is None:
        print(f"{'Status:':12} Weather unavailable")
        sep(length)
        return

    print(f"{'Location:':12} {weather['location']}")
    print(f"{'Condition:':12} {weather['weather']}")
    print(f"{'Temperature:':12} {weather['temp_c']}°C")
    print(f"{'Feels like:':12} {weather['feels_like']}°C")
    sep(length)
