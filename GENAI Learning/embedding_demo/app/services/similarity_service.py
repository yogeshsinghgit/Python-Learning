from loguru import logger
import numpy as np


class SimilarityService:

    @staticmethod
    def cosine_similarity(
        vector_1: list[float],
        vector_2: list[float],
    ) -> float:
        try:
            similarity = np.dot(
                vector_1,
                vector_2,
            ) / (
                np.linalg.norm(vector_1)
                * np.linalg.norm(vector_2)
            )

            return float(similarity)

        except Exception as exc:
            logger.exception(
                f"Similarity calculation failed: {exc}"
            )
            raise