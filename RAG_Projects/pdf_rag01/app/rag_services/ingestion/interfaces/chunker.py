"""
Base interface for all chunking strategies.
"""

from abc import ABC, abstractmethod

from app.schemas.document import Document
from app.schemas.chunk.chunk import Chunk


class Chunker(ABC):
    """
    Converts a parsed document into semantic chunks.
    """

    @abstractmethod
    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        """
        Split a document into chunks.

        Args:
            document: Preprocessed document.

        Returns:
            List of chunks.
        """
        raise NotImplementedError