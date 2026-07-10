"""
Mapper responsible for converting document elements into Chunk domain models.

The mapper encapsulates all Chunk creation logic, allowing chunkers to focus
only on determining chunk boundaries.
"""

from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

from app.schemas.chunk.chunk import Chunk
from app.schemas.chunk.enums import ChunkType
from app.schemas.chunk.metadata import ChunkMetadata

from app.schemas.document import (
    Document,
    DocumentElement,
)


class ChunkMapper:
    """Factory for creating Chunk domain objects."""

    @classmethod
    def from_elements(
        cls,
        *,
        document: Document,
        elements: list[DocumentElement],
        chunk_index: int,
        chunk_type: ChunkType = ChunkType.CONTENT,
        parent_chunk_id: str | None = None,
    ) -> Chunk:
        """
        Create a Chunk from a list of document elements.

        Args:
            document:
                Source document.

            elements:
                Elements belonging to this chunk.

            chunk_index:
                Sequential chunk number within the document.

            chunk_type:
                Logical chunk type.

            parent_chunk_id:
                Parent chunk identifier for hierarchical retrieval.

        Returns:
            Chunk domain object.
        """

        if not elements:
            raise ValueError(
                "Cannot create a chunk from an empty element list."
            )

        text = cls._combine_text(elements)

        first_element = elements[0]

        return Chunk(
            chunk_id=str(uuid4()),
            document_id=document.document_id,
            text=text,
            chunk_type=chunk_type,
            parent_chunk_id=parent_chunk_id,
            metadata=ChunkMetadata(
                chunk_index=chunk_index,
                page_number=first_element.page_number,
                character_count=len(text),
                element_count=len(elements),
            ),
            source_element_ids=[
                element.element_id
                for element in elements
                if element.element_id
            ],
        )

    @classmethod
    def from_existing_chunk(
        cls,
        *,
        chunk: Chunk,
        text: str,
        chunk_index: int,
        token_count: int,
    ) -> Chunk:
        """
        Create a new chunk by copying an existing chunk with updated text.

        Used by splitters to produce sub-chunks from an oversized parent,
        preserving all structural metadata (source elements, type, parent id)
        while updating positional fields.

        Args:
            chunk:
                Source chunk to copy structure from.

            text:
                New decoded text for this sub-chunk.

            chunk_index:
                Sequential index within the document.

            token_count:
                Pre-computed token count for this sub-chunk.

        Returns:
            New Chunk instance.
        """

        metadata = chunk.metadata.model_copy(
            update={
                "chunk_index": chunk_index,
                "token_count": token_count,
                "character_count": len(text),
            }
        )

        return Chunk(
            chunk_id=str(uuid4()),
            document_id=chunk.document_id,
            text=text,
            indexed_text=text if chunk.indexed_text is not None else None,
            chunk_type=chunk.chunk_type,
            metadata=metadata,
            source_element_ids=deepcopy(chunk.source_element_ids),
            parent_chunk_id=chunk.parent_chunk_id,
        )

    @staticmethod
    def _combine_text(
        elements: list[DocumentElement],
    ) -> str:
        """
        Combine element text while preserving paragraph separation.
        """

        return "\n\n".join(
            element.text
            for element in elements
        ).strip()