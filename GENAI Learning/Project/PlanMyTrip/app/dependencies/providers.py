from fastapi import Request
from redis.asyncio import Redis

from app.ai.travel_agent import TravelAgent
from app.dependencies.app_state import AppState
from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection


def get_app_state(request: Request) -> AppState:
    return request.app.state.app_state

def get_redis(request: Request) -> Redis:
    return request.app.state.app_state.redis

def get_llm(request: Request) -> ChatGroq:
    return request.app.state.app_state.llm

def get_checkpointer(request: Request) -> AsyncPostgresSaver:
    return request.app.state.app_state.checkpointer

def get_travel_agent(
    request: Request,
) -> TravelAgent:
    return request.app.state.app_state.travel_agent