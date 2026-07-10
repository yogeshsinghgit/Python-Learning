"""
Domain models representing parsed documents.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DocumentElementType(str, Enum):
    """
    Supported semantic document elements.
    """

    TITLE = "Title"

    NARRATIVE_TEXT = "NarrativeText"

    LIST_ITEM = "ListItem"

    TABLE = "Table"

    HEADER = "Header"

    FOOTER = "Footer"

    IMAGE = "Image"

    UNKNOWN = "Unknown"

class DocumentElement(BaseModel):
    """
    Represents a semantic element extracted from a document.
    """

    element_id: str

    element_type: DocumentElementType

    text: str

    page_number: int

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    @property
    def is_empty(self) -> bool:
        return not self.text.strip()


class DocumentMetadata(BaseModel):
    parser: str
    parser_version: str | None = None

    filename: str
    mime_type: str | None = None
    file_size_bytes: int

    page_count: int | None = None
    languages: list[str] = Field(default_factory=list)

    checksum: str

    ingested_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    document_created_at: datetime | None = None
    document_modified_at: datetime | None = None

    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    """
    Represents a parsed document.
    """

    document_id: str

    filename: str

    elements: list[DocumentElement]

    metadata: DocumentMetadata


    @property
    def text(self) -> str:
        """
        Return the complete document text.
        """

        return "\n".join(
            element.text
            for element in self.elements
        )