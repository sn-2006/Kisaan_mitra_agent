from google.adk.agents import Agent
import os
import requests
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()

def get_crop_price(commodity: str, market: str) -> str:
    """
    Fetch the latest crop price for a given commodity in a specific market using Data.gov.in API (Agmarknet).
    Returns a clean text summary.
    """
    api_key = os.getenv("DATAGOV_API_KEY")  # Set your API key in .env

    if not api_key:
        return "Error: Missing API key. Please set DATAGOV_API_KEY in your .env file."

    # Example API endpoint (data.gov.in Agmarknet daily prices dataset)
    url = (
        f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        f"?api-key={api_key}&format=json&filters[commodity]={commodity}&filters[market]={market}&limit=1&sort[date]=desc"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "records" not in data or len(data["records"]) == 0:
            return f"No data found for {commodity} in {market}."

        record = data["records"][0]
        min_price = record.get("min_price")
        max_price = record.get("max_price")
        modal_price = record.get("modal_price")
        date = record.get("date")

        return (
            f"Market Price for {commodity} in {market} (Date: {date}):\n"
            f"- Minimum Price: ₹{min_price}\n"
            f"- Maximum Price: ₹{max_price}\n"
            f"- Modal Price: ₹{modal_price}"
        )

    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    print(get_crop_price("Tomato", "Bengaluru"))

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
    tools=[get_crop_price],
)
