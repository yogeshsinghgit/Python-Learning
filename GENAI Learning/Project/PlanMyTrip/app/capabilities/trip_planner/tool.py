from typing import Any, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.capabilities.trip_planner.agent import TripPlannerAgent
from app.capabilities.trip_planner.schemas import TripPlanRequest


class TripPlannerToolInput(BaseModel):
    """
    Input schema for the trip planner tool.
    """

    destination: str = Field(
        description="The city or country to plan the trip for, e.g. 'Goa' or 'Paris'."
    )
    days: int = Field(
        description="The number of days for the trip, e.g. 3 or 5."
    )
    start_date: str | None = Field(
        default=None,
        description="The starting date of the trip in YYYY-MM-DD format (optional)."
    )


class TripPlannerTool(BaseTool):
    """
    Class-based tool adapting TripPlannerAgent to LangChain's tool interface.
    """

    name: str = "trip_planner"
    description: str = (
        "Generate a detailed day-by-day itinerary for a destination, "
        "including weather notes, attraction schedules, and hotel options. "
        "Use this tool when the user requests a complete trip plan or itinerary."
    )
    args_schema: Type[BaseModel] = TripPlannerToolInput
    agent: TripPlannerAgent

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError("TripPlannerTool only supports async execution.")

    async def _arun(
        self,
        destination: str,
        days: int,
        start_date: str | None = None,
    ) -> str:
        request = TripPlanRequest(
            destination=destination,
            days=days,
            start_date=start_date,
        )
        result = await self.agent.plan_trip(request)
        return result.model_dump_json()
