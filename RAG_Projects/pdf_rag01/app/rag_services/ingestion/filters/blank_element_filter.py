from __future__ import annotations

from loguru import logger

from app.rag_services.ingestion.interfaces.element_filter import ElementFilter
from app.schemas.document import Document


class BlankElementFilter(ElementFilter):
    """
    Removes document elements that contain no meaningful text.

    Filters out:
    - Empty strings
    - Whitespace-only strings
    - Newline-only strings
    - Tab-only strings
    """

    name = "blank_element_filter"

    async def filter(
        self,
        document: Document,
    ) -> Document:
        original_count = len(document.elements)

        document.elements = [
            element
            for element in document.elements
            if element.text.strip()
        ]

        removed = original_count - len(document.elements)

        logger.debug(
            f"{self.name}: removed {removed} blank elements "
            f"({original_count} -> {len(document.elements)})"
        )

        return document