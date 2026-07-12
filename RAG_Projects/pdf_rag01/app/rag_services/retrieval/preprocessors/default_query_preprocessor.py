from loguru import logger

from app.core.exceptions import ValidationError
from app.rag_services.retrieval.interfaces.query_preprocessor import (
    QueryPreprocessor,
)


class DefaultQueryPreprocessor(QueryPreprocessor):
    """
    Default query preprocessor.

    Current responsibilities:
        - Trim whitespace
        - Collapse multiple spaces
        - Validate empty queries

    Future responsibilities:
        - Lowercasing (optional)
        - Spell correction
        - Query rewriting
        - HyDE
        - Multi-query expansion
    """

    async def preprocess(self, query: str) -> str:
        logger.info("Starting query preprocessing.")

        try:
            if not isinstance(query, str):
                logger.error(f"Invalid query type: {type(query)}")
                raise ValidationError("Query must be a string.")

            # ---------------------------------------------------------
            # Remove leading and trailing whitespace
            # ---------------------------------------------------------
            normalized_query = query.strip()

            logger.debug(
                f"Query after strip(): '{normalized_query}'"
            )

            # ---------------------------------------------------------
            # Replace multiple spaces with a single space
            # ---------------------------------------------------------
            normalized_query = " ".join(normalized_query.split())

            logger.debug(
                f"Query after whitespace normalization: '{normalized_query}'"
            )

            # ---------------------------------------------------------
            # Validate query
            # ---------------------------------------------------------
            if not normalized_query:
                logger.warning("Received an empty query after preprocessing.")
                raise ValidationError(
                    "Query cannot be empty."
                )

            logger.success(
                f"Query preprocessing completed successfully. "
                f"Final query: '{normalized_query}'"
            )

            return normalized_query

        except ValidationException:
            raise

        except Exception as exc:
            logger.exception(
                f"Unexpected error while preprocessing query: {exc}"
            )
            raise