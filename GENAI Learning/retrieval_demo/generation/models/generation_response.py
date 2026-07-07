from pydantic import BaseModel, Field

from app.retrieval.models.retrieval_response import RetrievedChunk


class GenerationResponse(BaseModel):
    """Final response returned by the generation pipeline."""

    answer: str = Field(
        ...,
        description="Generated answer."
    )

    retrieved_chunks: list[RetrievedChunk] = Field(
        default_factory=list,
        description="Chunks used during generation."
    )

    prompt: PromptModel | None = Field(
        default=None,
        description="Prompt used for generation."
    )

    model: str = Field(
        default="",
        description="LLM model name."
    )

    latency_ms: float = Field(
        default=0.0,
        description="Generation latency."
    )