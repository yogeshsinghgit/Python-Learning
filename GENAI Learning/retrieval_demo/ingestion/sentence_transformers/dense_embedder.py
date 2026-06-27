import asyncio

from loguru import logger
from sentence_transformers import SentenceTransformer

from ingestion.interfaces.dense_embedder import DenseEmbedder


class SentenceTransformerDenseEmbedder(DenseEmbedder):
    def __init__(
        self,
        model_name: str,
    ) -> None:
        logger.info(f"Loading dense embedding model: {model_name}")

        self._model = SentenceTransformer(model_name)

        logger.success("Dense embedding model loaded successfully.")

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        try:
            logger.debug(
                f"Generating embedding for text length={len(text)}"
            )

            embedding = await asyncio.to_thread(
                self._model.encode,
                text,
                normalize_embeddings=True,
                convert_to_numpy=True,
            )

            return embedding.tolist()

        except Exception as exc:
            logger.exception(
                f"Failed to generate embedding: {exc}"
            )
            raise

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        try:
            logger.info(
                f"Generating embeddings for {len(texts)} texts."
            )

            embeddings = await asyncio.to_thread(
                self._model.encode,
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
            )

            return embeddings.tolist()

        except Exception as exc:
            logger.exception(
                f"Failed to generate batch embeddings: {exc}"
            )
            raise