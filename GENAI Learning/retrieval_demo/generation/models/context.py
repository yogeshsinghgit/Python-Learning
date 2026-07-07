from pydantic import BaseModel, Field


class ContextModel(BaseModel):
    """Represents the formatted context passed to the prompt builder."""

    context: str = Field(
        ...,
        description="Formatted context string."
    )

    chunk_count: int = Field(
        ...,
        ge=0,
        description="Number of unique chunks included."
    )

    character_count: int = Field(
        ...,
        ge=0,
        description="Total number of characters in the context."
    )