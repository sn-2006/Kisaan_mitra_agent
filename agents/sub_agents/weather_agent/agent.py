from google.adk.agents import Agent

import os
import requests
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()

def get_weather(city: str) -> str:
    """
    Fetch live weather information for a given city using OpenWeatherMap API.
    Returns a clean text summary.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "Error: Missing API key. Please set OPENWEATHER_API_KEY in your .env file."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"Error fetching data for {city}: {data.get('message', 'Unknown error')}."

        description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Weather in {city}:\n"
            f"- Condition: {description}\n"
            f"- Temperature: {temperature}°C (feels like {feels_like}°C)\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind_speed} m/s"
        )

    except Exception as e:
        return f"Error: {str(e)}"
weather_agent =Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="Provides weather updates, forecasts, and agricultural insights based on environmental conditions.",
    instruction="""
    You are the Weather Intelligence Agent of the KisaanMitra system.

    Your main responsibilities:
    - Provide accurate and concise weather forecasts.
    - Help farmers plan sowing, irrigation, and harvesting based on weather patterns.
    - Warn about extreme conditions like drought, heavy rainfall, or storms.
    - Suggest adaptive measures for changing weather.

    Guidelines:
    - Be direct and clear when giving forecasts or advice.
    - When possible, link weather conditions to farming actions (e.g., watering schedule, crop timing).
    - Use a supportive and informative tone.
    """,
    sub_agents=[],
    tools=[get_weather],
)
