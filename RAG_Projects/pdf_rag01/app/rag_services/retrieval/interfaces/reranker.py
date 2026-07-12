from abc import ABC, abstractmethod

from app.rag_services.retrieval.models.retrieval_result import (
    RetrievalResult,
)


class Reranker(ABC):
    """
    Defines the contract for reranking retrieved documents.
    """

    @abstractmethod
    async def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:
        """
        Reorder retrieval results based on relevance.

        Args:
            query: Original user query.
            results: Retrieved chunks.

        Returns:
            Reranked chunks.
        """
        raise NotImplementedError