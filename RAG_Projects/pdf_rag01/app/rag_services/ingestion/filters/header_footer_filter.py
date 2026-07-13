from loguru import logger

from app.rag_services.ingestion.interfaces.element_filter import ElementFilter
from app.schemas.document import (
    Document,
    DocumentElementType,
)


class HeaderFooterFilter(ElementFilter):
    """Removes elements classified as headers or footers."""

    name = "header_footer_filter"

    async def filter(self, document: Document) -> Document:
        original_count = len(document.elements)

        document.elements = [
            element
            for element in document.elements
            if element.element_type
            not in (
                DocumentElementType.HEADER,
                DocumentElementType.FOOTER,
            )
        ]

        removed = original_count - len(document.elements)

        logger.debug(
            f"{self.name}: removed {removed} elements "
            f"({original_count} -> {len(document.elements)})"
        )

        return document