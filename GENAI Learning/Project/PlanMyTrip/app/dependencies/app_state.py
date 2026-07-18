from dataclasses import dataclass

from app.ai.travel_agent import TravelAgent
from redis.asyncio import Redis
from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

@dataclass(slots=True)
class AppState:
    """
    Stores long-lived application resources.

    All shared dependencies should be initialized once during
    application startup and accessed through this object.
    """

    redis: Redis | None = None

    postgres: AsyncConnection | None = None

    llm: ChatGroq | None = None

    checkpointer: AsyncPostgresSaver | None = None

    travel_agent: TravelAgent | None = None

    # Future additions:
    # postgres_pool: AsyncConnectionPool | None = None
    # checkpointer: AsyncPostgresSaver | None = None
    # llm: ChatGroq | None = None
    # weather_client: WeatherClient | None = None



    