from dataclasses import dataclass

from app.ai.checkpointer import CheckpointerClient
from app.ai.llm import LLMClient
from app.ai.planner.service import PlannerService
from app.core.config import settings
from app.db.redis_client import RedisClient

from app.capabilities.attraction.client import AttractionClient
from app.capabilities.attraction.providers.open_trip_map import OpenTripMapAttractionProvider
from app.capabilities.weather.client import WeatherClient
from app.capabilities.weather.providers.open_meteo import OpenMeteoWeatherProvider

from app.tools import build_tool_registry, build_travel_tools
from app.capabilities.hotel.tool import hotel_search
from app.capabilities.trip_planner.tool import trip_planner

from app.ai.runtime_dependencies.graph_context import GraphContext


@dataclass(slots=True, frozen=True)
class AgentRuntime:
    """
    Shared runtime dependencies for all AI agents.
    """

    llm: LLMClient
    checkpointer: CheckpointerClient
    redis: RedisClient

    def create_graph_context(self) -> GraphContext:
        """
        Build the execution context passed to LangGraph nodes.
        """

        weather_client = WeatherClient(
            provider=OpenMeteoWeatherProvider()
        )

        attraction_client = AttractionClient(
            provider=OpenTripMapAttractionProvider(
                api_key=settings.OPEN_TRIP_MAP_API,
            )
        )

        tools = build_travel_tools(
            weather_client=weather_client,
            attraction_client=attraction_client,
            # Not yet migrated to the class-based pattern — still mocked.
            extra_tools=[hotel_search, trip_planner],
        )

        tool_registry = build_tool_registry(tools)

        planner = PlannerService(
            llm=self.llm.client,
            available_tools=list(tool_registry.keys()),
        )

        return GraphContext(
            llm=self.llm.client,
            redis=self.redis.client,
            planner=planner,
            tools=tools,
            tool_registry=tool_registry,
        )
