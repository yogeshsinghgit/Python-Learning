from app.tools.travel_tools import (
    attraction_search,
    hotel_search,
    trip_planner,
)

TRAVEL_TOOLS = [
    hotel_search,
    attraction_search,
    trip_planner,
]

TOOL_REGISTRY = {tool.name: tool for tool in TRAVEL_TOOLS}