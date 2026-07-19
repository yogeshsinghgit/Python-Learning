from dataclasses import dataclass

from app.ai.checkpointer import CheckpointerClient
from app.ai.llm import LLMClient
from app.db.redis_client import RedisClient


@dataclass(slots=True)
class AgentRuntime:
    """
    Shared runtime dependencies for all AI agents.
    """

    llm: LLMClient
    checkpointer: CheckpointerClient
    redis: RedisClient