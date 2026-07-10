"""
FastEmbed sparse embedding provider.
"""

import asyncio

from fastembed import SparseTextEmbedding
from loguru import logger

from app.core.config import get_settings
from app.core.exceptions import EmbeddingError
from app.infrastructure.embeddings.interfaces.sparse_embedder import (
    SparseEmbedder,
)
from app.infrastructure.vector_db.models import SparseVector


class FastEmbedSparseEmbedder(SparseEmbedder):

    def __init__(self) -> None:

        settings = get_settings()

        logger.info(
            f"Loading sparse embedding model '{settings.sparse_embedding_model}'."
        )

        self._model = SparseTextEmbedding(
            model_name=settings.sparse_embedding_model,
        )

        logger.success(
            "Sparse embedding model loaded successfully."
        )

    async def embed(
        self,
        text: str,
    ) -> SparseVector:

        try:

            logger.debug(
                f"Generating sparse embedding for text length={len(text)}."
            )

            embedding = await asyncio.to_thread(
                lambda: next(
                    self._model.embed([text])
                )
            )

            return SparseVector(
                indices=embedding.indices.tolist(),
                values=embedding.values.tolist(),
            )

        except Exception as exc:

            logger.exception(
                f"Failed generating sparse embedding: {exc}"
            )

            raise EmbeddingError(
                "Unable to generate sparse embedding."
            ) from exc

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[SparseVector]:

        try:

            logger.info(
                f"Generating sparse embeddings for {len(texts)} texts."
            )

            embeddings = await asyncio.to_thread(
                lambda: list(
                    self._model.embed(texts)
                )
            )

            return [
                SparseVector(
                    indices=embedding.indices.tolist(),
                    values=embedding.values.tolist(),
                )
                for embedding in embeddings
            ]

        except Exception as exc:

            logger.exception(
                f"Failed generating sparse embeddings: {exc}"
            )

            raise EmbeddingError(
                "Unable to generate sparse embeddings."
            ) from exc