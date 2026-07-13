from __future__ import annotations

import re

from loguru import logger

from app.rag_services.ingestion.interfaces.element_filter import ElementFilter
from app.schemas.document import Document


class PageNumberFilter(ElementFilter):
    """
    Removes standalone page number elements.

    Examples removed:

        12
        - 12 -
        Page 12
        12/420
        12 / 420
        12 of 420
        Page 12 of 420
    """

    name = "page_number_filter"

    _PAGE_NUMBER_PATTERN = re.compile(
        r"""
        ^
        (?:
            -?\s*\d+\s*-?                    # 12, -12-, - 12 -
            |
            Page\s+\d+                       # Page 12
            |
            \d+\s*/\s*\d+                    # 12/420
            |
            \d+\s+of\s+\d+                   # 12 of 420
            |
            Page\s+\d+\s+of\s+\d+            # Page 12 of 420
        )
        $
        """,
        re.IGNORECASE | re.VERBOSE,
    )


    @classmethod
    def _is_page_number(
        cls,
        text: str,
    ) -> bool:
        return bool(
            cls._PAGE_NUMBER_PATTERN.fullmatch(
                text.strip()
            )
        )
    
    async def filter(
        self,
        document: Document,
    ) -> Document:

        original_count = len(document.elements)

        document.elements = [
            element
            for element in document.elements
            if not self._is_page_number(element.text)
        ]

        removed = original_count - len(document.elements)

        logger.debug(
            f"{self.name}: removed {removed} page number elements "
            f"({original_count} -> {len(document.elements)})"
        )

        return document