from __future__ import annotations

import re

from loguru import logger

from app.rag_services.ingestion.interfaces.element_filter import ElementFilter
from app.schemas.document import Document

class FrontMatterFilter(ElementFilter):
    """
    Drops copyright/half-title/dedication-style pages that precede real
    content. Deliberately conservative: only removes a page if it has a
    strong keyword signal, or is extremely sparse AND within the first
    few pages. Never touches pages beyond `max_scan_pages`.
    """

    name = "front_matter_filter"

    _KEYWORDS = re.compile(
        r"(copyright\s*©|all rights reserved|isbn|library of congress|"
        r"printed in the united states|no part of this publication)",
        re.IGNORECASE,
    )

    def __init__(
        self,
        max_scan_pages: int = 10,
        sparse_word_limit: int = 25,
        sparse_page_limit: int = 4,
    ) -> None:
        self._max_scan_pages = max_scan_pages
        self._sparse_word_limit = sparse_word_limit
        self._sparse_page_limit = sparse_page_limit

    async def filter(self, document: Document) -> Document:
        original_count = len(document.elements)
        drop_pages: set[int] = set()

        for page_number, elements in document.pages.items():
            if page_number > self._max_scan_pages:
                break

            page_text = " ".join(e.text for e in elements if e.text.strip())
            if not page_text:
                continue

            word_count = len(page_text.split())
            has_keyword = bool(self._KEYWORDS.search(page_text))
            is_sparse_and_early = (
                page_number <= self._sparse_page_limit
                and word_count <= self._sparse_word_limit
            )

            if has_keyword or is_sparse_and_early:
                drop_pages.add(page_number)
                logger.debug(
                    f"{self.name}: page {page_number} flagged as front matter "
                    f"(keyword={has_keyword}, words={word_count})"
                )

        document.elements = [
            e for e in document.elements if e.page_number not in drop_pages
        ]

        removed = original_count - len(document.elements)
        logger.debug(
            f"{self.name}: removed {removed} elements across {len(drop_pages)} pages "
            f"({original_count} -> {len(document.elements)})"
        )
        return document