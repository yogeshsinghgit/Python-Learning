from langchain_core.tools import BaseTool

from app.capabilities.weather.client import WeatherClient
from app.capabilities.weather.tool import WeatherTool
from app.capabilities.attraction.client import AttractionClient
from app.capabilities.attraction.tool import AttractionTool


def build_travel_tools(
    *,
    weather_client: WeatherClient,
    attraction_client: AttractionClient,
    extra_tools: list[BaseTool] | None = None,
) -> list[BaseTool]:
    """
    Assemble the full set of tools available to the graph.

    Class-based tools (Weather, Attraction) are constructed here with
    their clients injected. `extra_tools` covers tools that haven't
    been migrated to the class-based pattern yet (currently:
    hotel_search, trip_planner — still mocked).
    """

    tools: list[BaseTool] = [
        WeatherTool(client=weather_client),
        AttractionTool(client=attraction_client),
    ]

    if extra_tools:
        tools.extend(extra_tools)

    return tools


def build_tool_registry(tools: list[BaseTool]) -> dict[str, BaseTool]:
    return {tool.name: tool for tool in tools}
