# agents/__init__.py

"""
KisaanMitra - AI Agents for Smarter Farming
Multi-agent system for agricultural advisory
"""


from .sub_agents.soil_agent import soil_agent
from .sub_agents.market_agent import market_agent
from .sub_agents.weather_agent import weather_agent

__all__ = [
    'soil_agent',
    'market_agent',
    'weather_agent'
]