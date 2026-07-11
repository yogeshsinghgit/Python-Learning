"""
Semantic element aware chunker.

Version 1 Rules:

- A TITLE starts a new chunk.
- All following elements belong to that chunk.
- Next TITLE closes the previous chunk.
- Preserve source element ids.
- Preserve first page number.
"""

from __future__ import annotations

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


class SemanticElementChunker(Chunker):
    """
    Chunk documents using semantic document boundaries.
    """

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
            if (
                element.element_type == DocumentElementType.TITLE
                and current_elements
            ):
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

    