from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RetrievalRequest(BaseModel):
    """
    Domain model representing a retrieval request.

    This model is independent of any vector database implementation.
    """

    model_config = ConfigDict(frozen=True)

    query: str = Field(
        ...,
        min_length=1,
        description="Natural language query.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Maximum number of chunks to retrieve.",
    )

    namespace: str | None = Field(
        default=None,
        description="Optional Pinecone namespace.",
    )

    metadata_filter: dict[str, Any] | None = Field(
        default=None,
        description="Optional metadata filter.",
    )