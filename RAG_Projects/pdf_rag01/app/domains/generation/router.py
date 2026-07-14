
from fastapi import APIRouter, Depends, status
from loguru import logger

from .models import GenerationRequest, GenerationResult
from .services import GenerationService

router = APIRouter(
    prefix="/query",
    tags=["Generation"],
)


@router.post("")
async def query(
    request: GenerationRequest,
    service: GenerationService = Depends(
        get_generation_service
    ),
):

    return await service.generate(
        request
    )