from abc import ABC, abstractmethod

from retrieval.models.search_query import SearchQuery
from retrieval.models.retrieved_chunk import RetrievedChunk


class SearchRepository(ABC):
    """
    Contract for vector database search operations.
    """

    @abstractmethod
    async def dense_search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """
        Execute dense vector similarity search.

        Args:
            query: Search request.

        Returns:
            SearchResult ordered by descending similarity.
        """
        raise NotImplementedError

    @abstractmethod
    async def sparse_search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """
        Execute sparse vector similarity search.

        Args:
            query: Search request.

        Returns:
            SearchResult ordered by descending similarity.
        """
        raise NotImplementedError