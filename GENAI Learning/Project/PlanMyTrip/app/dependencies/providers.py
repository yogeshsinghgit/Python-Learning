from fastapi import Request, Depends
from redis.asyncio import Redis

from app.ai.agents.travel_agent import TravelAgent
from app.dependencies.app_state import AppState
from langchain_groq import ChatGroq

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

from app.services.chat_service import ChatService


def get_app_state(request: Request) -> AppState:
    return request.app.state.app_state

def get_redis(request: Request) -> Redis:
    return request.app.state.app_state.redis

def get_llm(request: Request) -> ChatGroq:
    return request.app.state.app_state.llm

def get_checkpointer(request: Request) -> AsyncPostgresSaver:
    return request.app.state.app_state.checkpointer


def get_travel_agent(
    app_state: AppState = Depends(get_app_state),
) -> TravelAgent:
    return app_state.travel_agent

def get_chat_service(request: Request) -> ChatService:
    return ChatService(
        travel_agent=request.app.state.app_state.travel_agent
    )