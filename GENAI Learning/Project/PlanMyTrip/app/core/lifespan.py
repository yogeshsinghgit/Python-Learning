from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from redis.asyncio import Redis

from app.core.config import settings
from app.core.logging import configure_logging
from app.dependencies.app_state import AppState
from app.ai.travel_agent import TravelAgent

from app.db.redis_client import connect_redis, disconnect_redis
from app.db.postgres_client import connect_postgres, disconnect_postgres
from app.graph.checkpointer import get_checkpointer
from app.graph.llm import get_llm



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize and dispose application resources.
    """

    configure_logging()

    logger.info("Starting AI Travel Agent...")

    app_state = AppState()

    try:

        app_state.postgres = await connect_postgres()
        logger.success("Postgres Connected")

        logger.info("Connecting to Redis...")

        app_state.redis = await connect_redis()

        logger.success("Redis connected successfully.")

        app_state.llm = get_llm()
        logger.success("LLM Connected")

        app_state.checkpointer = await get_checkpointer()
        logger.success("Checkpointer Ready")

        app_state.travel_agent = TravelAgent(
            llm=app_state.llm,
            checkpointer=app_state.checkpointer,
        )

        app.state.app_state = app_state

        logger.success("Application startup completed.")

        yield

    except Exception as exc:
        logger.exception(f"Application startup failed: {exc}")
        raise

    finally:
        logger.info("Shutting down application...")

        if app_state.redis is not None:
            await disconnect_redis()
            logger.info("Redis connection closed.")

        if app_state.postgres is not None:
            await disconnect_postgres()
            logger.info("Postgres connection closed.")

        logger.success("Application shutdown completed.")