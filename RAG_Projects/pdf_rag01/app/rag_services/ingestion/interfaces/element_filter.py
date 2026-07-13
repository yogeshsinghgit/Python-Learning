from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.document import Document


class ElementFilter(ABC):
    """
    Contract for document element filters.

    An ElementFilter receives the entire document, performs any
    filtering or modification on its elements, and returns the
    updated document.

    Implementations should modify only `document.elements` and
    preserve the document metadata.
    """

    name: str

    async def __call__(self, document: Document) -> Document:
        return await self.filter(document)

    @abstractmethod
    async def filter(self, document: Document) -> Document:
        """
        Apply the filter to the document.

        Args:
            document: The document to filter.

        Returns:
            The filtered document.
        """
        raise NotImplementedError