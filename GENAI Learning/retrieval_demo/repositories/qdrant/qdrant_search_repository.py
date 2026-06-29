from loguru import logger
from qdrant_client import AsyncQdrantClient

from repositories.interfaces.search_repository import SearchRepository
from retrieval.models.search_query import SearchQuery
from retrieval.models.retrieved_chunk import RetrievedChunk


class QdrantSearchRepository(SearchRepository):
    """
    Qdrant implementation of SearchRepository.
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
        raise NotImplementedError