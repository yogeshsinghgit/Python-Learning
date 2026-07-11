from pydantic import BaseModel, ConfigDict


class UploadResponse(BaseModel):
    """
    Response returned after successful document ingestion.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    message: str

    document_id: str

    filename: str

    chunk_count: int

    vector_count: int

    processing_time_ms: float