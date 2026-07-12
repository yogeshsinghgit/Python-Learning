from loguru import logger

from app.rag_services.retrieval.interfaces.reranker import (
    Reranker,
)
from app.rag_services.retrieval.models.retrieval_result import (
    RetrievalResult,
)


class DefaultReranker(Reranker):
    """
    Default reranker.

    Performs no reranking and returns the results unchanged.
    """

    async def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:

        logger.info(
            f"NoOpReranker received {len(results)} retrieval results."
        )

        if not results:
            logger.warning(
                "No retrieval results available for reranking."
            )
            return results

        logger.debug(
            "Skipping reranking and returning results unchanged."
        )

        logger.success(
            f"Returning {len(results)} retrieval results."
        )

        return results