from loguru import logger

from app.infrastructure.vector_db.models import QueryResult
from app.rag_services.retrieval.models.retrieval_result import RetrievalResult


class RetrievalResultMapper:
    """
    Maps vector repository query results into retrieval domain models.
    """

    def _map(self, result: QueryResult) -> RetrievalResult:
        """
        Convert a single QueryResult into a RetrievalResult.
        """

        logger.debug(
            f"Mapping QueryResult -> RetrievalResult "
            f"(id='{result.id}', score={result.score:.4f})"
        )

        return RetrievalResult(
            chunk_id=result.id,
            text=result.text,
            score=result.score,
            metadata=result.metadata,
        )

    def map_many(
        self,
        results: list[QueryResult],
    ) -> list[RetrievalResult]:
        """
        Convert multiple QueryResults into RetrievalResults.
        """

        logger.info(
            f"Mapping {len(results)} query results."
        )

        mapped_results = [
            self._map(result)
            for result in results
        ]

        logger.success(
            f"Successfully mapped {len(mapped_results)} retrieval results."
        )

        return mapped_results