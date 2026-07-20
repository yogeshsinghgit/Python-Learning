from pydantic import BaseModel, Field


class TripPlanRequest(BaseModel):
    """
    Input schema for the trip planner capability.
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


class DayPlan(BaseModel):
    """
    Structured plan for a single day of the trip.
    """

    day_number: int = Field(
        description="The day number, starting at 1."
    )
    date: str = Field(
        description="The date of the plan, e.g. 'Day 1' or a specific date if start_date is known."
    )
    weather_note: str = Field(
        description="A brief description of weather expectations and its impact on the itinerary."
    )
    attractions: list[str] = Field(
        description="List of attractions or activities visited during this day."
    )
    hotel_note: str = Field(
        description="Details/options for hotel/stay."
    )


class TripPlan(BaseModel):
    """
    Full structured day-by-day trip plan.
    """

    destination: str = Field(
        description="The destination of the trip."
    )
    days: list[DayPlan] = Field(
        description="List of daily plans for the trip."
    )
