import asyncio

from loguru import logger

from app.infrastructure.embeddings.interfaces.dense_embedder import DenseEmbedder
from app.infrastructure.embeddings.interfaces.sparse_embedder import SparseEmbedder
from app.rag_services.retrieval.models.query_vector import QueryVector



class QueryVectorBuilder:
    """
    Builds dense and sparse query vectors concurrently.
    """

    def __init__(
        self,
        dense_embedder: DenseEmbedder,
        sparse_embedder: SparseEmbedder,
    ) -> None:
        self._dense_embedder = dense_embedder
        self._sparse_embedder = sparse_embedder

    async def build(self, query: str) -> QueryVector:
        """
        Generate dense and sparse vectors for a query.
        """

        logger.info(
            f"Generating embeddings for query: '{query}'"
        )

        try:
            dense_task = asyncio.create_task(
                self._dense_embedder.embed(query)
            )

            sparse_task = asyncio.create_task(
                self._sparse_embedder.embed(query)
            )

            dense_vector, sparse_vector = await asyncio.gather(
                dense_task,
                sparse_task,
            )

            logger.debug(
                f"Dense embedding dimension: {len(dense_vector)}"
            )

            logger.debug(
                f"Sparse embedding contains "
                f"{len(sparse_vector.indices)} non-zero values."
            )

            logger.success(
                "Successfully generated query embeddings."
            )

            return QueryVector(
                dense = dense_vector,
                sparse = sparse_vector
            )


        except Exception as exc:
            logger.exception(
                f"Failed to generate query embeddings: {exc}"
            )
            raise