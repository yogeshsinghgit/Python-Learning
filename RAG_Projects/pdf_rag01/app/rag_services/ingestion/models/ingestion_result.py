from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class IngestionResult(BaseModel):
    """
    Result returned after a successful document ingestion.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    document_id: str

    filename: str

    chunk_count: int

    vector_count: int

    checksum: str

    processing_time_ms: float

    success: bool = True