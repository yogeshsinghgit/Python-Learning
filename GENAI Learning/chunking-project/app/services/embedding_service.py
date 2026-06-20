from sentence_transformers import SentenceTransformer
from loguru import logger

from app.schemas.chunk import Chunk
from app.schemas.embedded_chunk import EmbeddedChunk


class EmbeddingService:

    def __init__(self) -> None:

        self._model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        logger.info(
            "Embedding model initialized"
        )

    async def generate_embedding(
        self,
        chunk: Chunk,
    ) -> EmbeddedChunk:

        try:

            logger.info(
                f"Generating embedding "
                f"for chunk {chunk.chunk_id}"
            )

            vector = self._model.encode(
                chunk.content
            ).tolist()

            return EmbeddedChunk(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                vector=vector,
            )

        except Exception as exc:

            logger.exception(
                f"Embedding generation failed: {exc}"
            )

            raise