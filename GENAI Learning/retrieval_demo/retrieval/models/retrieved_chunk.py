from typing import Any

from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    """
    Represents one retrieved document chunk.
    """

    id: str = Field(
        ...,
        description="Unique chunk identifier.",
    )

    content: str = Field(
        ...,
        description="Chunk text.",
    )

    score: float = Field(
        ...,
        description="Similarity score returned by the vector database.",
    )

    rrf_score: float | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Chunk metadata.",
    )