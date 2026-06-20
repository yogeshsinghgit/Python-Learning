from sentence_transformers import SentenceTransformer
from loguru import logger


class EmbeddingService:
    def __init__(self) -> None:
        logger.info(
            "Loading SentenceTransformer model: all-MiniLM-L6-v2 "
            "(downloading ~90MB on first run, please wait...)"
        )
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.success("Model loaded successfully!")

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        try:
            logger.info(f"Generating embedding for: {text}")

            embedding = self.model.encode(text)

            logger.info(
                f"Embedding dimension: {len(embedding)}"
            )

            return embedding.tolist()

        except Exception as exc:
            logger.exception(
                f"Embedding generation failed: {exc}"
            )
            raise