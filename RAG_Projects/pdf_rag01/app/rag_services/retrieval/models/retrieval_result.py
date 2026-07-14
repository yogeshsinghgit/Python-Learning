from pydantic import BaseModel, ConfigDict, Field


class RetrievalResult(BaseModel):
    """
    Represents a retrieved chunk.
    """

    model_config = ConfigDict(frozen=True)

    chunk_id: str

    text: str

    score: float

    metadata: dict[str, object] = Field(default_factory=dict)


class RetrievalContext(BaseModel):
    results: list[RetrievalResult]
    total_results: int