from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import ScoredPoint

from core.constants import DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME, CONTENT_FIELD, METADATA_FIELD
from exceptions.repository_exception import RepositoryException
from retrieval.interfaces.search_repository import SearchRepository
from retrieval.models.retrieved_chunk import RetrievedChunk
from retrieval.models.search_query import SearchQuery


class QdrantSearchRepository(SearchRepository):
    """
    Qdrant implementation of the SearchRepository.
    """

    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str,
    ) -> None:
        self._client = client
        self._collection_name = collection_name

    async def dense_search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """
        Execute dense vector similarity search.
        """

        logger.info(
            f"Executing dense search on collection '{self._collection_name}'."
        )

        try:
            response = await self._client.query_points(
                collection_name=self._collection_name,
                query=query.dense_vector,
                using=DENSE_VECTOR_NAME,
                limit=query.top_k,
                score_threshold=query.score_threshold,
                query_filter=query.metadata_filter,
                with_payload=True,
                with_vectors=False,
            )

            results = [
                self._map_scored_point(point)
                for point in response.points
            ]

            logger.info(
                f"Dense search completed successfully. Retrieved {len(results)} chunks."
            )

            return results

        except Exception as exc:
            logger.exception(
                f"Failed to execute dense search: {exc}"
            )

            raise RepositoryException(
                "Failed to execute dense search."
            ) from exc

    async def sparse_search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:

        logger.info(
            f"Executing sparse search on collection '{self._collection_name}'."
        )

        try:
            response = await self._client.query_points(
                collection_name=self._collection_name,
                query=query.sparse_vector,
                using=SPARSE_VECTOR_NAME,
                limit=query.top_k,
                score_threshold=query.score_threshold,
                query_filter=query.metadata_filter,
                with_payload=True,
                with_vectors=False,
            )

            results = [
                self._map_scored_point(point)
                for point in response.points
            ]

            logger.info(
                f"Sparse search completed successfully. Retrieved {len(results)} chunks."
            )

            return results

        except Exception as exc:
            logger.exception(
                f"Failed to execute sparse search: {exc}"
            )

            raise RepositoryException(
                "Failed to execute sparse search."
            ) from exc

    @staticmethod
    def _map_scored_point(
        point: ScoredPoint,
    ) -> RetrievedChunk:
        """
        Convert a Qdrant ScoredPoint into a RetrievedChunk.
        """

        payload = point.payload or {}

        logger.info(f"Payload: {payload}")

        return RetrievedChunk(
            id=str(point.id),
            content=payload.get(CONTENT_FIELD, ""),
            score=point.score,
            metadata=payload,
        )