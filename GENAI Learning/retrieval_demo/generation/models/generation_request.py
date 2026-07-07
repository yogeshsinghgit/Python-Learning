from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    """User query for RAG generation."""

    query: str = Field(
        ...,
        description="Original user query."
    )