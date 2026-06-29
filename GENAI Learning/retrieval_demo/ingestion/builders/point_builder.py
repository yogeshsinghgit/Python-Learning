import asyncio

from loguru import logger

from ingestion.interfaces.dense_embedder import DenseEmbedder
from ingestion.interfaces.sparse_embedder import SparseEmbedder
from schemas.chunk import Chunk
from schemas.point import HybridPoint
from schemas.vectors import DenseVector, SparseVectorData


class PointBuilder:

    def __init__(
        self,
        dense_embedder: DenseEmbedder,
        sparse_embedder: SparseEmbedder,
    ) -> None:

        self._dense_embedder = dense_embedder
        self._sparse_embedder = sparse_embedder

    async def build(self, chunk: Chunk) -> HybridPoint:

        logger.debug(
            f"Building point for chunk '{chunk.chunk_id}'"
        )

        dense_task = self._dense_embedder.embed(
            chunk.text
        )

        sparse_task = self._sparse_embedder.embed(
            chunk.text
        )

        dense_vector, sparse_vector = await asyncio.gather(
            dense_task,
            sparse_task,
        )

        indices, values = sparse_vector

        payload = {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "text": chunk.text,
            **chunk.metadata,
        }

        dense = DenseVector(
            values=dense_vector,
        )

        sparse = SparseVectorData(
            indices=indices,
            values=values,
        )

        return HybridPoint(
            point_id=chunk.chunk_id,
            dense=dense,
            sparse=sparse,
            payload=payload,
        )

    async def build_batch(self, chunks: list[Chunk]) -> list[HybridPoint]:

        if not chunks:
            return []

        logger.info(
            f"Building {len(chunks)} hybrid points."
        )

        texts = [
            chunk.text
            for chunk in chunks
        ]

        dense_task = self._dense_embedder.embed_batch(
            texts
        )

        sparse_task = self._sparse_embedder.embed_batch(
            texts
        )

        dense_vectors, sparse_vectors = await asyncio.gather(
            dense_task,
            sparse_task,
        )

        points: list[HybridPoint] = []

        for chunk, dense_vector, sparse_vector in zip(
            chunks,
            dense_vectors,
            sparse_vectors,
            strict=True,
        ):

            indices, values = sparse_vector
            dense = DenseVector(
                values=dense_vector,
            )

            sparse = SparseVectorData(
                indices=indices,
                values=values,
            )

            payload = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "text": chunk.text,
                **chunk.metadata,
            }

            points.append(
                HybridPoint(
                    point_id=chunk.chunk_id,
                    dense=dense,
                    sparse=sparse,
                    payload=payload,
                )
            )

        logger.success(
            f"Successfully built {len(points)} hybrid points."
        )

        return points
