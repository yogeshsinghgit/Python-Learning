from pydantic import BaseModel, ConfigDict, Field


class RetrievalRequestBody(BaseModel):
    """
    HTTP request model for document retrieval.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    query: str = Field(
        ...,
        min_length=1,
        description="User query.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of chunks to retrieve.",
    )


class RetrievalResponse(BaseModel):
    """
    HTTP response model.
    """

    context: str

    chunk_ids: list[str]

    total_chunks: int