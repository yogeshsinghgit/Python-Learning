from pydantic import BaseModel, Field


class LLMResult(BaseModel):
    """Normalized response returned by any LLM provider."""

    answer: str = Field(
        ...,
        description="Generated response from the LLM."
    )

    model: str = Field(
        ...,
        description="Model used for generation."
    )

    input_tokens: int = Field(
        default=0,
        ge=0,
        description="Number of input tokens."
    )

    output_tokens: int = Field(
        default=0,
        ge=0,
        description="Number of generated tokens."
    )

    total_tokens: int = Field(
        default=0,
        ge=0,
        description="Total token usage."
    )

    finish_reason: str = Field(
        default="unknown",
        description="Reason generation finished."
    )