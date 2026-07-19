from dataclasses import dataclass

from app.ai.agents.travel_agent import TravelAgent
from app.ai.llm import LLMClient
from app.ai.checkpointer import CheckpointerClient
from app.db.postgres_client import PostgresClient
from app.db.redis_client import RedisClient

@dataclass(slots=True)
class AppState:
    """
    Stores long-lived application resources.

    All shared dependencies should be initialized once during
    application startup and accessed through this object.
    """

    redis: RedisClient | None = None

    postgres: PostgresClient | None = None

    llm: LLMClient | None = None

    checkpointer: CheckpointerClient | None = None

    travel_agent: TravelAgent | None = None

    # Future additions:
    # postgres_pool: AsyncConnectionPool | None = None
    # checkpointer: AsyncPostgresSaver | None = None
    # llm: ChatGroq | None = None
    # weather_client: WeatherClient | None = None



    