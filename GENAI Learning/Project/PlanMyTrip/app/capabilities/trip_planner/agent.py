import asyncio
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from loguru import logger

from app.capabilities.attraction.client import AttractionClient
from app.capabilities.hotel.tool import hotel_search
from app.capabilities.trip_planner.exceptions import TripPlannerError
from app.capabilities.trip_planner.prompts import TRIP_PLANNER_PROMPT
from app.capabilities.trip_planner.schemas import TripPlan, TripPlanRequest
from app.capabilities.weather.client import WeatherClient


class TripPlannerAgent:
    """
    Coordinates weather, attraction, and hotel information to generate a
    structured, day-by-day trip plan using a dedicated structured output LLM call.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        weather_client: WeatherClient,
        attraction_client: AttractionClient,
        hotel_search_fn: Any = None,
    ) -> None:
        self._llm = llm.with_structured_output(TripPlan)
        self._weather_client = weather_client
        self._attraction_client = attraction_client
        self._hotel_search = hotel_search_fn or hotel_search

    async def plan_trip(self, request: TripPlanRequest) -> TripPlan:
        logger.info(
            "Planning trip to '{}' for {} days, starting: {}",
            request.destination,
            request.days,
            request.start_date,
        )

        try:
            # 1. Fetch weather and attractions concurrently
            weather_task = self._weather_client.get_weather(request.destination)
            attraction_task = self._attraction_client.search_attractions(
                request.destination
            )

            weather_res, attraction_res = await asyncio.gather(
                weather_task, attraction_task
            )

            # 2. Fetch mocked hotel search. If it is a tool or a custom callable, run it appropriately.
            if hasattr(self._hotel_search, "ainvoke"):
                hotel_res = await self._hotel_search.ainvoke(
                    {"destination": request.destination}
                )
            else:
                hotel_res = await self._hotel_search(request.destination)

            logger.debug("Gathered external capability contexts for planning.")

            # Formulate contexts for prompt
            weather_desc = (
                f"Location: {weather_res.location}\n"
                f"Temp: {weather_res.temperature_celsius}°C\n"
                f"Wind: {weather_res.windspeed_kmh} km/h\n"
                f"Description: {weather_res.weather_description}"
            )

            attractions_list = [
                f"- {att.name}: {att.description or 'No description'} (Rating: {att.rating or 'N/A'}, Address: {att.formatted_address or 'N/A'})"
                for att in attraction_res.attractions
            ]
            attractions_desc = (
                "\n".join(attractions_list)
                if attractions_list
                else "No attractions found."
            )

            hotel_desc = str(hotel_res)

            # 3. Call structured output LLM
            prompt = TRIP_PLANNER_PROMPT.invoke(
                {
                    "destination": request.destination,
                    "days": request.days,
                    "start_date": request.start_date or "unspecified",
                    "weather_context": weather_desc,
                    "attractions_context": attractions_desc,
                    "hotel_context": hotel_desc,
                }
            )

            logger.info("Invoking structured LLM for TripPlan synthesis...")
            trip_plan = await self._llm.ainvoke(prompt)
            logger.success("TripPlan successfully synthesized.")
            return trip_plan

        except Exception as exc:
            logger.exception(
                "Failed to generate trip plan for destination: {}",
                request.destination,
            )
            raise TripPlannerError(
                f"Failed to generate trip plan: {exc}"
            ) from exc
