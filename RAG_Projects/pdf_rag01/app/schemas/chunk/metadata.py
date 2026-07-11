from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):

    chunk_index: int

    page_number: int | None = None

    section_title: str | None = None

    token_count: int | None = None

    character_count: int | None = None

    element_count: int | None = None

    # extra_metadata: dict[str, Any] = Field(default_factory=dict)