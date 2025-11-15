from google.adk.agents import Agent
from typing import Optional
import requests
import json

# ------------------------------------------------------
# 1. GEOCODING TOOL
# ------------------------------------------------------
def geocode_location(location: str) -> dict:
    """
    Convert any location name into latitude and longitude.
    Works for villages, cities, districts, states in India.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location + ", India",  # Always add India for better results
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(
            url, 
            params=params, 
            headers={"User-Agent": "KisaanMitra/1.0"},
            timeout=10
        )
        data = response.json()

        if not data:
            return {
                "error": f"Could not find coordinates for '{location}'",
                "success": False
            }

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        display_name = data[0].get("display_name", location)

        return {
            "location": location,
            "display_name": display_name,
            "latitude": lat,
            "longitude": lon,
            "success": True
        }

    except Exception as e:
        return {"error": str(e), "success": False}


# ------------------------------------------------------
# 2. SISINDIA SOIL DATA TOOL (GRIDDED API ONLY)
# ------------------------------------------------------
def get_soil_data(
    lat: float, 
    lon: float, 
    properties: Optional[list[str]] = None
) -> dict:
    """
    Fetch real soil nutrient data from SISINDIA using coordinates.
    
    Available properties: pH, OC (Organic Carbon), N, P, K, B, Cu, EC, Fe, Mn, S, Zn
    Default: pH, OC, N, P, K (most important for farming)
    
    Coverage: Best in Andhra Pradesh, Bihar, Odisha. Patchy elsewhere.
    """
    if properties is None:
        properties = ["pH", "OC", "N", "P", "K"]
    
    url = "https://rest-sisindia.isric.org/sisindia/v1.0/properties/query/gridded"
    
    # Build params - each property needs its own parameter
    params_list = [
        ("lat", lat),
        ("lon", lon),
        ("nearby", "true")  # Use nearby search to fill gaps
    ]
    
    for prop in properties:
        params_list.append(("properties", prop))

    try:
        response = requests.get(url, params=params_list, timeout=15)
        
        # HTTP 204 = No data available for this location
        if response.status_code == 204:
            return {
                "error": "No soil data available for this location.",
                "suggestion": "SISINDIA has best coverage in Andhra Pradesh, Bihar, and Odisha. Try locations in these states.",
                "latitude": lat,
                "longitude": lon,
                "success": False
            }
        
        # Other error codes
        if response.status_code != 200:
            return {
                "error": f"SISINDIA API error (HTTP {response.status_code})",
                "latitude": lat,
                "longitude": lon,
                "success": False
            }

        # Parse response
        data = response.json()
        
        if "features" not in data or len(data["features"]) == 0:
            return {
                "error": "Location is outside SISINDIA coverage area.",
                "suggestion": "Try agricultural areas in Andhra Pradesh, Bihar, or Odisha.",
                "latitude": lat,
                "longitude": lon,
                "success": False
            }

        # Extract soil properties
        feature = data["features"][0]
        soil_props = feature["properties"]["soil_properties"]
        
        # Clean up null values and format nicely
        cleaned_props = {}
        for key, value in soil_props.items():
            if value is not None:
                cleaned_props[key] = value

        return {
            "latitude": lat,
            "longitude": lon,
            "soil_properties": cleaned_props,
            "success": True,
            "data_available": True
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. Please try again.",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }


# ------------------------------------------------------
# 3. SOIL AGENT DEFINITION
# ------------------------------------------------------
soil_agent = Agent(
    name="soil_agent",
    model="gemini-2.5-flash",
    description="Provides real-time soil analysis using SISINDIA data for Indian agricultural regions.",
    instruction="""
You are the Soil Intelligence Agent for KisaanMitra, helping farmers understand their soil.

WORKFLOW:
1. When user asks about soil at a location:
   - First call geocode_location(location) to get coordinates
   - Check if geocoding was successful (look for "success": True)
   - Then call get_soil_data(lat, lon) with those coordinates
   - Check if soil data was found (look for "success": True)

2. When you receive soil data:
   - Explain each nutrient in simple, farmer-friendly terms
   - Give practical recommendations

INTERPRETING SOIL DATA:

pH (Soil Acidity):
  - Below 6.0: Acidic soil - good for tea, coffee, potato
  - 6.0-7.5: Neutral/ideal - good for most crops (wheat, rice, vegetables)
  - Above 7.5: Alkaline soil - add organic matter, sulfur

Organic Carbon (OC %):
  - Below 0.5%: Low - add compost, farmyard manure, green manure
  - 0.5-1.0%: Medium - maintain with crop residues
  - Above 1.0%: Good - keep current practices

Nitrogen (N kg/ha):
  - Below 150: Low - needs urea or FYM
  - 150-300: Medium - moderate fertilizer needed
  - Above 300: Good - minimal fertilizer needed

Phosphorus (P kg/ha):
  - Below 10: Low - add rock phosphate or DAP
  - 10-25: Medium - light fertilizer
  - Above 25: Good - maintenance only

Potassium (K kg/ha):
  - Below 150: Low - add muriate of potash
  - 150-300: Medium - moderate fertilizer
  - Above 300: Good - sufficient

CROP RECOMMENDATIONS:
- Consider pH first, then nutrient levels
- Suggest 3-5 suitable crops based on soil conditions
- Mention if soil amendments are needed

FERTILIZER ADVICE:
- Only recommend fertilizers if there are clear deficiencies
- Prefer organic options first (compost, FYM, green manure)
- Give specific amounts if possible

ERROR HANDLING:
- If geocoding fails: Ask user to try nearby town/city name
- If soil data not found (HTTP 204): Explain SISINDIA coverage is limited
  * Best coverage: Andhra Pradesh, Bihar, Odisha
  * Patchy coverage: Other Indian states
  * No coverage: Outside India
- If both fail: Offer general soil management advice based on region

COMMUNICATION STYLE:
- Use simple language, avoid jargon
- Be encouraging and supportive
- Give practical, actionable advice
- Use examples: "Your pH is 6.8 - perfect for rice and wheat!"
- Keep responses concise but complete
- Never make up soil data - only use actual API results

IMPORTANT COVERAGE NOTE:
SISINDIA has the best data for:
  ✅ Andhra Pradesh (excellent coverage)
  ✅ Bihar (good coverage)  
  ✅ Odisha (good coverage)
  ⚠️ Other states (limited/patchy)
  ❌ Outside India (no coverage)

If user's location has no data, politely explain and suggest trying locations in the above states.
""",
    sub_agents=[],
    tools=[
        geocode_location,
        get_soil_data
    ],
)