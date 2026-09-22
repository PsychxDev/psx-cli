import json
import socket
from urllib import error, request
from urllib.parse import quote

from psx.utils.display import header, sep


def _has_internet_connection() -> bool:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def _fetch_weather(location: str | None = None) -> dict | None:
    if not _has_internet_connection():
        return None

    if location and location.strip():
        url = f"https://wttr.in/{quote(location.strip())}?format=j1"
    else:
        url = "https://wttr.in/?format=j1"

    try:
        request_obj = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with request.urlopen(request_obj, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (error.URLError, ValueError, TimeoutError):
        return None

    current = (payload.get("current_condition") or [{}])[0]
    if not current:
        return None

    weather_desc = (
        current.get("weatherDesc", [{"value": "Unknown"}])[0].get("value", "Unknown")
    )
    temp_c = current.get("temp_C", "Unknown")
    feels_like = current.get("FeelsLikeC", "Unknown")

    area = payload.get("nearest_area") or [{"areaName": [{"value": "Unknown"}]}]
    location_name = area[0].get("areaName", [{"value": "Unknown"}])[0].get("value", "Unknown")

    return {
        "location": location_name or (location or "Current location"),
        "weather": weather_desc,
        "temp_c": temp_c,
        "feels_like": feels_like,
    }


def run(location: str | None = None) -> None:
    length = header("Weather")
    weather = _fetch_weather(location)

    if weather is None:
        target = location.strip() if location and location.strip() else "current location"
        print(f"{'Status:':12} Weather unavailable for {target}")
        sep(length)
        return

    print(f"{'Location:':12} {weather['location']}")
    print(f"{'Condition:':12} {weather['weather']}")
    print(f"{'Temperature:':12} {weather['temp_c']}°C")
    print(f"{'Feels like:':12} {weather['feels_like']}°C")
    sep(length)