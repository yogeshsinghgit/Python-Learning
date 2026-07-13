
from __future__ import annotations
"""
Semantic element aware chunker.

Version 1 Rules:

- A TITLE starts a new chunk.
- All following elements belong to that chunk.
- Next TITLE closes the previous chunk.
- Preserve source element ids.
- Preserve first page number.
"""

"""
Semantic element aware chunker.

Version 2 Rules:

- A TITLE marks a candidate chunk boundary.
- The current chunk is only closed when a new TITLE arrives AND the
  buffer already has at least `min_body_words` of non-title text.
  This prevents consecutive/short TITLE runs (e.g. chapter + subtitle,
  or TOC-style heading lists) from producing heading-only chunks.
- Preserve source element ids.
- Preserve first page number.
"""



from uuid import uuid4

from loguru import logger

from app.rag_services.ingestion.interfaces.chunker import Chunker
from app.rag_services.ingestion.mappers.chunk_mapper import ChunkMapper

from app.schemas.chunk.chunk import Chunk
from app.schemas.chunk.metadata import ChunkMetadata
from app.schemas.chunk.enums import ChunkType
from app.schemas.document import (
    Document,
    DocumentElement,
    DocumentElementType,
)

_NON_BODY_TYPES = {DocumentElementType.TITLE, DocumentElementType.HEADER, DocumentElementType.FOOTER}


class SemanticElementChunker(Chunker):
    """
    Chunk documents using semantic document boundaries.
    """

    def __init__(self, min_body_words: int = 15) -> None:
        self._min_body_words = min_body_words

    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:

        logger.info(
            f"Starting semantic chunking for document "
            f"'{document.filename}'."
        )

        chunks: list[Chunk] = []
        current_elements: list[DocumentElement] = []
        chunk_index = 0

        for element in document.elements:
            # Skip empty text defensively.
            if not element.text.strip():
                continue

            # New title means current chunk is complete.
            is_title = element.element_type == DocumentElementType.TITLE

            if is_title and current_elements:
                if self._body_word_count(current_elements) >= self._min_body_words:
                    chunks.append(
                        ChunkMapper.from_elements(
                            document=document,
                            elements=current_elements,
                            chunk_index=chunk_index,
                        )
                    )

                    logger.debug(
                        f"Created chunk index={chunk_index} "
                        f"with {len(current_elements)} elements."
                    )

                    chunk_index += 1
                    current_elements = []
                else:
                    logger.debug(
                        "New TITLE encountered but current buffer has "
                        f"< {self._min_body_words} body words — merging "
                        "as additional heading instead of splitting."
                    )
                    # fall through: title gets appended to current buffer below
            current_elements.append(element)

        # Flush remaining elements.
        if current_elements:

            chunks.append(
                ChunkMapper.from_elements(
                    document=document,
                    elements=current_elements,
                    chunk_index=chunk_index,
                )
            )

            logger.debug(
                f"Created final chunk index={chunk_index} "
                f"with {len(current_elements)} elements."
            )

        logger.info(
            f"Chunking completed. "
            f"Generated {len(chunks)} chunks "
            f"from {len(document.elements)} document elements."
        )

        return chunks

    @staticmethod
    def _body_word_count(elements: list[DocumentElement]) -> int:
        """Word count excluding TITLE elements — headings alone don't count as body content."""
        return sum(
            len(e.text.split())
            for e in elements
            if e.element_type if e.element_type not in _NON_BODY_TYPES
        )

    