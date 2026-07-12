from pydantic import BaseModel, ConfigDict, Field


class LLMContext(BaseModel):
    """
    Context prepared for the LLM.
    """

    model_config = ConfigDict(frozen=True)

    context: str

    chunk_ids: list[str] = Field(default_factory=list)

    total_chunks: int = 0