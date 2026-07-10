"""
VectorDocument Builder.

Responsible for converting document chunks
into VectorDocument objects.
"""

import asyncio

from loguru import logger

from app.infrastructure.embeddings.interfaces.dense_embedder import (
    DenseEmbedder,
)
from app.infrastructure.embeddings.interfaces.sparse_embedder import (
    SparseEmbedder,
)
from app.infrastructure.embeddings.mapper import (
    create_vector_document,
)
from app.infrastructure.vector_db.models import (
    VectorDocument,
)
from app.schemas.chunk import Chunk


class VectorDocumentBuilder:
    """
    Builds VectorDocument objects from document chunks.
    """

    def __init__(
        self,
        dense_embedder: DenseEmbedder,
        sparse_embedder: SparseEmbedder,
    ) -> None:

        self._dense_embedder = dense_embedder
        self._sparse_embedder = sparse_embedder

    async def build(
        self,
        chunk: Chunk,
    ) -> VectorDocument:
        """
        Build a VectorDocument for a single chunk.
        """

        logger.debug(
            f"Building VectorDocument for chunk '{chunk.chunk_id}'."
        )

        text = chunk.indexed_text or chunk.text

        dense_task = self._dense_embedder.embed(
            text,
        )

        sparse_task = self._sparse_embedder.embed(
            text,
        )

        dense_vector, sparse_vector = await asyncio.gather(
            dense_task,
            sparse_task,
        )

        logger.success(
            f"Successfully built VectorDocument for chunk '{chunk.chunk_id}'."
        )

        return create_vector_document(
            chunk=chunk,
            dense_vector=dense_vector,
            sparse_vector=sparse_vector,
        )

    async def build_batch(
        self,
        chunks: list[Chunk],
    ) -> list[VectorDocument]:
        """
        Build VectorDocuments for multiple chunks.
        """

        if not chunks:
            logger.warning(
                "No chunks provided for VectorDocument generation."
            )
            return []

        logger.info(
            f"Building {len(chunks)} VectorDocuments."
        )

        texts = [
            chunk.text
            for chunk in chunks
        ]

        dense_task = self._dense_embedder.embed_batch(
            texts,
        )

        sparse_task = self._sparse_embedder.embed_batch(
            texts,
        )

        dense_vectors, sparse_vectors = await asyncio.gather(
            dense_task,
            sparse_task,
        )

        documents = [
            create_vector_document(
                chunk=chunk,
                dense_vector=dense_vector,
                sparse_vector=sparse_vector,
            )
            for chunk, dense_vector, sparse_vector in zip(
                chunks,
                dense_vectors,
                sparse_vectors,
                strict=True,
            )
        ]

        logger.success(
            f"Successfully built {len(documents)} VectorDocuments."
        )

        return documents