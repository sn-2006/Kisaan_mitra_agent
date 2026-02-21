from google.adk.agents import Agent
import pandas as pd
from datetime import datetime
from typing import Optional

# Load CSV once at startup
df = pd.read_csv("data/commodity_price.csv")

def get_market_price(
    commodity: str,
    state: str,
    district: Optional[str] = None,
    market: Optional[str] = None
) -> dict:
    """
    Fetch market price from local mandi dataset with fuzzy matching.
    """

    data = df.copy()

    # Normalize user inputs
    commodity = commodity.lower().strip()
    state = state.lower().strip()

    if district:
        district = district.lower().replace("district", "").strip()

    if market:
        market = market.lower().strip()

    # Commodity: PARTIAL MATCH
    data = data[data["Commodity"].str.lower().str.contains(commodity)]

    # State: EXACT MATCH
    data = data[data["State"].str.lower() == state]

    # District: PARTIAL MATCH
    if district:
        data = data[data["District"].str.lower().str.contains(district)]

    # Market: PARTIAL MATCH
    if market:
        data = data[data["Market"].str.lower().str.contains(market)]

    if data.empty:
        return {
            "error": "No matching market data found",
            "debug_hint": {
                "commodity": commodity,
                "state": state,
                "district": district,
                "market": market
            }
        }

    # Latest by date
    data["Arrival_Date"] = pd.to_datetime(
        data["Arrival_Date"], format="%d/%m/%Y", errors="coerce"
    )
    latest = data.sort_values("Arrival_Date").iloc[-1]

    return {
        "commodity": latest["Commodity"],
        "state": latest["State"],
        "district": latest["District"],
        "market": latest["Market"],
        "variety": latest["Variety"],
        "min_price": int(latest["Min_x0020_Price"]),
        "max_price": int(latest["Max_x0020_Price"]),
        "modal_price": int(latest["Modal_x0020_Price"]),
        "arrival_date": str(latest["Arrival_Date"].date()),
        "source": "local_csv_dataset",
        "timestamp": datetime.utcnow().isoformat()
    }
# 🔥 ADK Agent (UNCHANGED, just better tool)
market_agent = Agent(
    name="market_agent",
    model="gemini-2.5-flash",
    description="Analyzes crop market prices and gives selling insights using mandi data.",
    instruction="""
    You are the Market Intelligence Agent of the KisaanMitra system.

    Responsibilities:
    - Provide crop prices from mandi data.
    - Help farmers choose best markets and selling time.
    - Explain prices in simple, farmer-friendly language.
    - Suggest actions based on price trends.

    Rules:
    - Be clear and practical.
    - If data is missing, ask for more location details.
    - Avoid technical jargon.
    """,
    tools=[get_market_price],
)