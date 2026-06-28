from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: str

    source: Path

    content: str

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )