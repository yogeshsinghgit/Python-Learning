from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class PlannerRequest(BaseModel):
    """
    Input provided to the planner.

    The planner should make its decision using the latest user
    query together with any conversational context available.

    Today:
        - query
        - history

    Future:
        - retrieved_context
        - user_profile
        - conversation_summary
        - current_itinerary
    """

    query: str = Field(
        description="Latest user message."
    )

    history: list[BaseMessage] = Field(
        default_factory=list,
        description="Conversation history available to the planner.",
    )


class PlannerIntent(str, Enum):
    """
    High-level user intents understood by the planner.
    """

    CHAT = "chat"

    WEATHER = "weather"

    HOTEL_SEARCH = "hotel_search"

    FLIGHT_SEARCH = "flight_search"

    ATTRACTION_SEARCH = "attraction_search"

    TRIP_PLANNING = "trip_planning"


class PlannerDecision(BaseModel):
    """
    Structured decision returned by the planner.

    This object is consumed by the LangGraph planner node
    to determine graph routing.
    """

    intent: PlannerIntent

    should_use_tools: bool = Field(
        description="Whether downstream tool execution is required."
    )

    tool_names: list[str] = Field(
        default_factory=list,
        description="Names of tools that should be executed.",
    )

    extracted_entities: dict[str, Any] = Field(
        default_factory=dict,
        description="Relevant structured information extracted from the query.",
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    reasoning: str = Field(
        description="Short explanation for debugging and observability."
    )