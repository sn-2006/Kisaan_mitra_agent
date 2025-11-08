# agent.py (Root Orchestrator)
from google.adk.agents import Agent
from agents.sub_agents.market_agent.agent import market_agent
from agents.sub_agents.soil_agent.agent import soil_agent
from agents.sub_agents.weather_agent.agent import weather_agent
# Simple import from agents package


# 🧠 Define the Root Agent (main coordinator)
root_agent = Agent(
    name="agents",
    model="gemini-2.5-flash",  # or use your configured model variable
    description="Root agent that coordinates between soil, weather, and market intelligence agents for the KisaanMitra project.",
    instruction=f"""
    You are the main coordinator agent for KisaanMitra, an AI system designed to help farmers make smarter decisions.

    You work together with three specialized agents:
    1. Soil Agent — provides insights on soil quality, type, and recommendations.
    2. Weather Agent — gives weather forecasts and environmental data.
    3. Market Agent — provides real-time crop pricing and market analysis.

    Workflow:
    - When a user asks about soil conditions or improvement methods, delegate the task to the Soil Agent.
    - When a user asks about weather forecasts, rainfall, or ideal sowing times, delegate the task to the Weather Agent.
    - When a user asks about crop prices or selling strategies, delegate the task to the Market Agent.
    - Combine insights from multiple agents when needed to provide a complete recommendation.
    """,
    sub_agents=[
        soil_agent,
        weather_agent,
        market_agent,
    ],
)
