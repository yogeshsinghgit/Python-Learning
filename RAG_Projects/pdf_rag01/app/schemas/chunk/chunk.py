from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.chunk.enums import ChunkType
from app.schemas.chunk.metadata import ChunkMetadata


class Chunk(BaseModel):
    """
    Represents a semantic chunk produced from a document.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    chunk_id: str

    document_id: str

    # Original chunk content returned to the LLM.
    text: str

    # Text used for embedding. If None, `text` will be embedded.
    indexed_text: str | None = None

    chunk_type: ChunkType = ChunkType.CONTENT

    metadata: ChunkMetadata

    source_element_ids: list[str] = Field(default_factory=list)

    parent_chunk_id: str | None = None