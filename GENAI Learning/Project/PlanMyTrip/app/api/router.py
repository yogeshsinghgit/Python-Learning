from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.chat import (
    router as chat_router,
)
from app.core.constants import API_V1_PREFIX

api_router = APIRouter(prefix=API_V1_PREFIX)

api_router.include_router(health_router)

api_router.include_router(chat_router)