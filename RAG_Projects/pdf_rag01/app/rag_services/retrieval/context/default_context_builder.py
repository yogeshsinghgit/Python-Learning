from loguru import logger

from app.rag_services.retrieval.interfaces.context_builder import (
    ContextBuilder,
)
from app.rag_services.retrieval.models.llm_context import (
    LLMContext,
)
from app.rag_services.retrieval.models.retrieval_result import (
    RetrievalResult,
)


class DefaultContextBuilder(ContextBuilder):
    """
    Default implementation that concatenates retrieved chunks.
    """

    async def build(
        self,
        results: list[RetrievalResult],
    ) -> LLMContext:

        logger.info(
            f"Building LLM context from {len(results)} chunks."
        )

        if not results:
            logger.warning(
                "No retrieval results received."
            )

            return LLMContext(
                context="",
                chunk_ids=[],
                total_chunks=0,
            )

        context = "\n\n".join(
            result.text
            for result in results
        )

        chunk_ids = [
            result.chunk_id
            for result in results
        ]

        logger.success(
            f"Successfully built context containing "
            f"{len(chunk_ids)} chunks."
        )

        return LLMContext(
            context=context,
            chunk_ids=chunk_ids,
            total_chunks=len(results),
        )