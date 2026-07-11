"""
Default implementation of the document preprocessor.

Responsibilities:
- Remove empty elements.
- Normalize whitespace.
- Preserve semantic structure.
- Return a NEW Document instance.
"""

from __future__ import annotations

from loguru import logger

from app.rag_services.ingestion.interfaces.document_preprocessor import (
    DocumentPreprocessor
)
from app.rag_services.ingestion.utils.text_normalizer import TextNormalizer
from app.schemas.document import Document


class DefaultDocumentPreprocessor(DocumentPreprocessor):
    """
    Production-ready document preprocessor.

    This implementation intentionally performs only safe preprocessing.
    """

    async def preprocess(
        self,
        document: Document,
    ) -> Document:
        """
        Clean parsed document before chunking.
        """

        logger.info(
            f"Preprocessing document '{document.filename}'."
        )

        cleaned_elements = []

        removed_empty = 0

        for element in document.elements:

            normalized_text = TextNormalizer.normalize(
                element.text,
            )

            # Ignore elements that become empty after normalization.
            if not normalized_text:
                removed_empty += 1
                continue

            cleaned_elements.append(
                element.model_copy(
                    update={
                        "text": normalized_text,
                    }
                )
            )

        logger.info(
            f"Document preprocessing completed. "
            f"Original elements={len(document.elements)}, "
            f"Remaining={len(cleaned_elements)}, "
            f"Removed={removed_empty}"
        )

        return document.model_copy(
            update={
                "elements": cleaned_elements,
            }
        )