from loguru import logger

from app.rag_services.retrieval.models.retrieval_request import (
    RetrievalRequest,
)
from app.rag_services.retrieval.pipeline.retrieval_pipeline import (
    RetrievalPipeline,
)

from .models import (
    RetrievalRequestBody,
    RetrievalResponse,
)


class RetrievalService:

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
    ) -> None:
        self._pipeline = retrieval_pipeline

    async def retrieve(
        self,
        request: RetrievalRequestBody,
    ) -> RetrievalResponse:

        logger.info(
            f"Received retrieval request: '{request.query}'"
        )

        llm_context = await self._pipeline.retrieve(
            RetrievalRequest(
                query=request.query,
                top_k=request.top_k,
            )
        )

        logger.success(
            f"Successfully retrieved {llm_context.total_chunks} chunks."
        )

        return RetrievalResponse(
            context=llm_context.context,
            chunk_ids=llm_context.chunk_ids,
            total_chunks=llm_context.total_chunks,
        )