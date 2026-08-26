import requests


# -----------------------------------------
# GET CITY COORDINATES
# -----------------------------------------

def get_coordinates(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"]
    }


# -----------------------------------------
# WEATHER CONDITION
# -----------------------------------------

def weather_condition(code):

    conditions = {

        0: "Clear Sky",

        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing Rime Fog",

        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",

        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",

        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",

        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",

        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Thunderstorm with Hail"
    }

    return conditions.get(
        code,
        "Unknown"
    )


# -----------------------------------------
# GET LIVE WEATHER
# -----------------------------------------

def get_weather(city):

    location = get_coordinates(city)

    if location is None:
        return None

    latitude = location["latitude"]
    longitude = location["longitude"]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "weather_code"
        ),

        "forecast_days": 7,

        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {

        "city": location["name"],

        "temperature": current[
            "temperature_2m"
        ],

        "humidity": current[
            "relative_humidity_2m"
        ],

        "wind_speed": current[
            "wind_speed_10m"
        ],

        "condition": weather_condition(
            current["weather_code"]
        ),

        "forecast": data.get(
            "daily",
            {}
        )
    }