from fastapi import APIRouter, Depends

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.dependencies.providers import (
    get_chat_service,
)
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(
        get_chat_service,
    ),
):

    response = await service.chat(
        thread_id=request.thread_id,
        message=request.message,
    )

    return ChatResponse(
        response=response,
    )