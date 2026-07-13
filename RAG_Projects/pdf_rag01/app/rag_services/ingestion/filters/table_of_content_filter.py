from __future__ import annotations

import re

from loguru import logger

from app.rag_services.ingestion.interfaces.element_filter import ElementFilter
from app.schemas.document import Document


class TableOfContentsFilter(ElementFilter):
    """
    Drops entire pages that look structurally like a Table of Contents.

    Works on lines, not elements, because `unstructured` sometimes emits
    a whole TOC page as a single NarrativeText blob with embedded
    newlines rather than one element per entry.

    A page is flagged if:
      - it contains a "Contents" / "Table of Contents" heading line, OR
      - a high enough fraction of its lines look like "<title> <page num>"
        entries, within a minimum count.
    Only the first `max_scan_pages` are ever considered — TOCs don't
    appear in the middle of a document.
    """

    name = "table_of_contents_filter"

    _HEADING_LINE = re.compile(
        r"^(table of contents|contents|index)\s*$", re.IGNORECASE
    )

    # short-ish line, ending in a 1-4 digit number, optionally with
    # dot/dash/space leaders. Deliberately loose because unstructured
    # strips formatting inconsistently.
    _ENTRY_LINE = re.compile(
        r"^(?=.{2,80}$)(?:\d+(\.\d+)*\s+)?\S.*?[\.\-\s]\s*\d{1,4}$"
    )

    def __init__(
        self,
        max_scan_pages: int = 20,
        score_threshold: float = 0.5,
        min_entries: int = 3,
    ) -> None:
        self._max_scan_pages = max_scan_pages
        self._score_threshold = score_threshold
        self._min_entries = min_entries

    async def filter(self, document: Document) -> Document:
        original_count = len(document.elements)
        toc_pages: set[int] = set()

        for page_number, elements in document.pages.items():
            if page_number > self._max_scan_pages:
                break

            lines = [
                line.strip()
                for el in elements
                for line in el.text.split("\n")
                if line.strip()
            ]
            if not lines:
                continue

            has_heading = any(self._HEADING_LINE.match(l) for l in lines[:3])
            entry_hits = sum(1 for l in lines if self._ENTRY_LINE.match(l))
            score = entry_hits / len(lines)

            if has_heading or (
                entry_hits >= self._min_entries and score >= self._score_threshold
            ):
                toc_pages.add(page_number)
                logger.debug(
                    f"{self.name}: page {page_number} flagged as TOC "
                    f"(entries={entry_hits}/{len(lines)}, heading={has_heading})"
                )

        document.elements = [
            e for e in document.elements if e.page_number not in toc_pages
        ]

        removed = original_count - len(document.elements)
        logger.debug(
            f"{self.name}: removed {removed} elements across {len(toc_pages)} pages "
            f"({original_count} -> {len(document.elements)})"
        )
        return document