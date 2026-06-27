import asyncio

from fastembed import SparseTextEmbedding
from loguru import logger

from ingestion.interfaces.sparse_embedder import SparseEmbedder


class FastEmbedSparseEmbedder(SparseEmbedder):
    def __init__(
        self,
        model_name: str,
    ) -> None:
        logger.info(
            f"Loading sparse embedding model: {model_name}"
        )

        self._model = SparseTextEmbedding(
            model_name=model_name,
        )

        logger.success(
            "Sparse embedding model loaded successfully."
        )

    async def embed(
        self,
        text: str,
    ) -> tuple[list[int], list[float]]:
        try:
            logger.debug(
                f"Generating sparse embedding for text length={len(text)}"
            )

            sparse_embedding = await asyncio.to_thread(
                lambda: next(
                    self._model.embed([text])
                )
            )

            return (
                sparse_embedding.indices.tolist(),
                sparse_embedding.values.tolist(),
            )

        except Exception as exc:
            logger.exception(
                f"Failed generating sparse embedding: {exc}"
            )
            raise

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[tuple[list[int], list[float]]]:
        try:
            logger.info(
                f"Generating sparse embeddings for {len(texts)} texts."
            )

            sparse_embeddings = await asyncio.to_thread(
                lambda: list(
                    self._model.embed(texts)
                )
            )

            return [
                (
                    embedding.indices.tolist(),
                    embedding.values.tolist(),
                )
                for embedding in sparse_embeddings
            ]

        except Exception as exc:
            logger.exception(
                f"Failed generating sparse batch embeddings: {exc}"
            )
            raise