from __future__ import annotations

from typing import Any

from unstructured.documents.elements import Element

from app.ingestion.models.document_element import DocumentElement
from app.ingestion.models.enums import DocumentElementType


class UnstructuredElementMapper:
    """
    Maps Unstructured elements into internal domain models.
    """

    _TYPE_MAPPING = {
        "Title": DocumentElementType.TITLE,
        "NarrativeText": DocumentElementType.NARRATIVE_TEXT,
        "Table": DocumentElementType.TABLE,
        "ListItem": DocumentElementType.LIST_ITEM,
        "Header": DocumentElementType.HEADER,
        "Footer": DocumentElementType.FOOTER,
        "Image": DocumentElementType.IMAGE,
    }

    @classmethod
    def map(cls, element: Element) -> DocumentElement:
        """
        Convert an Unstructured element into a domain model.
        """

        element_type = cls._TYPE_MAPPING.get(
            element.category,
            DocumentElementType.UNKNOWN,
        )

        metadata: dict[str, Any] = {}

        if element.metadata:
            metadata = element.metadata.to_dict()

        return DocumentElement(
            id=getattr(element, "id", None),
            type=element_type,
            text=element.text or "",
            page_number=getattr(element.metadata, "page_number", None),
            metadata=metadata,
        )