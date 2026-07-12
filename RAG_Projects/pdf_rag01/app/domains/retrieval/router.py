from fastapi import APIRouter, Depends, status
from loguru import logger

from .models import (
    RetrievalRequestBody,
    RetrievalResponse,
)
from app.domains.retrieval.services import RetrievalService
from app.rag_services.dependencies.retrieval import get_retrieval_service


router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.post(
    "/search",
    response_model=RetrievalResponse,
    status_code=status.HTTP_200_OK,
)
async def search_documents(
    request: RetrievalRequestBody,
    retrieval_service: RetrievalService = Depends(
        get_retrieval_service,
    ),
) -> RetrievalResponse:

    logger.info(
        f"Received retrieval request for '{request.query}'."
    )

    response = await retrieval_service.retrieve(
        request,
    )

    logger.success(
        "Retrieval completed successfully."
    )

    return response