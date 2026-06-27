from typing import Any

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    chunk_id: str
    document_id: str

    text: str

    metadata: dict[str, Any] = Field(default_factory=dict)