"""
Base interface for document preprocessing.

A document preprocessor is responsible for cleaning and normalizing
parsed document elements before chunking.

The preprocessor must NOT:
- Generate chunks
- Remove semantic meaning
- Perform embedding

It only prepares a clean Document for downstream processing.
"""

from abc import ABC, abstractmethod

from app.schemas.document import Document


class DocumentPreprocessor(ABC):
    """Abstract base class for document preprocessors."""

    @abstractmethod
    async def preprocess(
        self,
        document: Document,
    ) -> Document:
        """
        Preprocess a parsed document.

        Args:
            document: Parsed document.

        Returns:
            Cleaned document.
        """
        raise NotImplementedError