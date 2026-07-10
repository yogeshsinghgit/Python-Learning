"""
SentenceTransformer dense embedding provider.
"""

import asyncio

from loguru import logger
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.core.exceptions import EmbeddingError
from app.infrastructure.embeddings.interfaces.dense_embedder import (
    DenseEmbedder,
)
from app.infrastructure.vector_db.models import DenseVector


class SentenceTransformerDenseEmbedder(DenseEmbedder):

    def __init__(self) -> None:

        settings = get_settings()

        logger.info(
            f"Loading dense embedding model '{settings.embedding_model}'."
        )

        self._model = SentenceTransformer(
            settings.embedding_model,
        )

        logger.success(
            "Dense embedding model loaded successfully."
        )

    async def embed(
        self,
        text: str,
    ) -> DenseVector:

        try:

            logger.debug(
                f"Generating dense embedding for text length={len(text)}."
            )

            embedding = await asyncio.to_thread(
                self._model.encode,
                text,
                normalize_embeddings=True,
                convert_to_numpy=True,
            )

            return DenseVector(
                values=embedding.tolist(),
            )

        except Exception as exc:

            logger.exception(
                f"Failed generating dense embedding: {exc}"
            )

            raise EmbeddingError(
                "Unable to generate dense embedding."
            ) from exc

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[DenseVector]:

        try:

            logger.info(
                f"Generating dense embeddings for {len(texts)} texts."
            )

            embeddings = await asyncio.to_thread(
                self._model.encode,
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
            )

            return [
                DenseVector(values=embedding.tolist())
                for embedding in embeddings
            ]

        except Exception as exc:

            logger.exception(
                f"Failed generating dense embeddings: {exc}"
            )

            raise EmbeddingError(
                "Unable to generate dense embeddings."
            ) from exc

    async def dimension(self) -> int:

        return self._model.get_sentence_embedding_dimension()