import asyncio

from loguru import logger

from qdrant_client.http.models import SparseVector

from ingestion.interfaces.dense_embedder import DenseEmbedder
from ingestion.interfaces.sparse_embedder import SparseEmbedder
from retrieval.interfaces.search_repository import SearchRepository
from retrieval.models.retrieved_chunk import RetrievedChunk
from retrieval.models.search_query import SearchQuery
from retrieval.services.rrf_service import RRFService


class RetrievalService:
    """
    Orchestrates the complete hybrid retrieval pipeline.
    """

    def __init__(
        self,
        dense_embedder: DenseEmbedder,
        sparse_embedder: SparseEmbedder,
        search_repository: SearchRepository,
        rrf_service: RRFService,
    ) -> None:
        self._dense_embedder = dense_embedder
        self._sparse_embedder = sparse_embedder
        self._search_repository = search_repository
        self._rrf_service = rrf_service

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:

        logger.info(
            f"Starting hybrid retrieval for query: '{query}'"
        )

        #
        # Generate embeddings concurrently
        #
        dense_vector, sparse_vector = await asyncio.gather(
            self._dense_embedder.embed(query),
            self._sparse_embedder.embed(query),
        )

        dense_query = SearchQuery(
            dense_vector=dense_vector,
            top_k=top_k,
        )

        sparse_indices, sparse_values = sparse_vector

        sparse_query = SearchQuery(
            sparse_vector=SparseVector(
                indices=sparse_indices,
                values=sparse_values,
            ),
            top_k=top_k,
        )

        #
        # Execute both searches concurrently
        #
        dense_results, sparse_results = await asyncio.gather(
            self._search_repository.dense_search(
                dense_query,
            ),
            self._search_repository.sparse_search(
                sparse_query,
            ),
        )

        logger.info(
            f"Dense returned {len(dense_results)} results."
        )

        logger.info(
            f"Sparse returned {len(sparse_results)} results."
        )

        fused_results = self._rrf_service.fuse(
            dense_results=dense_results,
            sparse_results=sparse_results,
            top_k=top_k,
        )

        logger.info(
            f"Hybrid retrieval returned {len(fused_results)} results."
        )

        return fused_results