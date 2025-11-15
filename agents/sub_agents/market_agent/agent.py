from google.adk.agents import Agent
import os
import requests
from dotenv import load_dotenv


from datetime import datetime
from typing import Optional

def get_market_price(
    commodity: str,
    state: str,
    district: Optional[str] = None,
    market: Optional[str] = None
) -> dict:
    """
    Fetch market price for a commodity using Data.gov.in Mandi dataset.
    """

    api_key = os.getenv("DATA_GOV_IN_KEY")
    if not api_key:
        return {"error": "DATA_GOV_IN_KEY missing in .env file"}

    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": api_key,
        "format": "json",
        "limit": 1,
    }

    # required filters
    params["filters[Commodity]"] = commodity
    params["filters[State]"] = state

    # optional
    if district:
        params["filters[District]"] = district
    if market:
        params["filters[Market]"] = market

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
    except Exception as e:
        return {"error": f"Failed to fetch or parse data: {e}"}

    if "records" not in data or not data["records"]:
        return {"error": "No records found for given filters"}

    rec = data["records"][0]

    def get_field(field):
        return rec.get(field) or rec.get(field.replace(" ", "_")) or rec.get(field.lower())

    return {
        "commodity": get_field("Commodity"),
        "state": get_field("State"),
        "district": get_field("District"),
        "market": get_field("Market"),
        "variety": get_field("Variety"),
        "grade": get_field("Grade"),
        "arrival_date": get_field("Arrival Date") or get_field("Arrival_Date"),
        "min_price": get_field("Min X0020 Price") or get_field("Min_X0020_Price"),
        "max_price": get_field("Max X0020 Price") or get_field("Max_X0020_Price"),
        "modal_price": get_field("Modal X0020 Price") or get_field("Modal_X0020_Price"),
        "timestamp": datetime.utcnow().isoformat()
    }

market_agent = Agent(
    name="market_agent",
    model="gemini-2.5-flash",
    description="Analyzes market data, predicts price trends, and offers crop selling strategies.",
    instruction="""
    You are the Market Intelligence Agent of the KisaanMitra system.

    Your main responsibilities:
    - Provide real-time or general crop price information.
    - Suggest the best times and locations to sell produce.
    - Offer insights on demand, supply, and profit optimization.
    - Help farmers make better selling and storage decisions.

    Guidelines:
    - Be data-driven yet easy to understand.
    - Offer actionable insights, not just numbers.
    - If market data is missing, ask for location or crop details.
    - Keep responses simple, farmer-oriented, and optimistic.
    """,
    sub_agents=[],
    tools=[get_market_price],
)
