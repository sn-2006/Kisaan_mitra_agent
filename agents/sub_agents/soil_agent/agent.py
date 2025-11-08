from google.adk.agents import Agent
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_soil_data(lat: float, lon: float) -> str:
    """
    Fetch soil temperature and moisture data using AgroMonitoring API.
    Requires latitude and longitude as input.
    """
    api_key = os.getenv("AGRO_API_KEY")

    if not api_key:
        return "Error: Missing AGRO_API_KEY. Please set it in your .env file."

    url = f"https://api.agromonitoring.com/agro/1.0/soil?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"Error fetching data: {data.get('message', 'Unknown error')}"

        # Extract key data safely
        temperature = data.get("t0", "N/A")       # top layer temperature (Kelvin)
        moisture = data.get("moisture", "N/A")    # volumetric soil moisture (m3/m3)

        if temperature != "N/A":
            temperature = round(temperature - 273.15, 2)  # Convert Kelvin → Celsius

        return (
            f"Soil data for {lat}, {lon}:\n"
            f"- Soil Temperature: {temperature}°C\n"
            f"- Soil Moisture: {moisture} m³/m³\n"
            f"(Data from AgroMonitoring API)"
        )

    except Exception as e:
        return f"Error fetching soil data: {str(e)}"
soil_agent = Agent(
    name="soil_agent",
    model="gemini-2.5-flash",
    description="Analyzes soil data and provides insights on soil quality, crop suitability, and fertilizer recommendations.",
    instruction="""
    You are the Soil Intelligence Agent of the KisaanMitra system.

    Your main responsibilities:
    - Analyze soil quality and pH levels.
    - Suggest suitable crops based on soil type and region.
    - Recommend fertilizers, organic matter, and soil enhancement methods.
    - Guide farmers on soil health maintenance and crop rotation.

    Guidelines:
    - Keep your answers practical, concise, and farmer-friendly.
    - Use simple language, no heavy technical jargon.
    - When details are missing (e.g., soil type or pH), ask for them clearly.
    """,
    sub_agents=[],
    tools=[get_soil_data],
)
