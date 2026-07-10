"""
Base interface for document loaders.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.document import Document


class DocumentLoader(ABC):
    """
    Base interface for all document loaders.
    """

    @abstractmethod
    async def load(
        self,
        file_path: Path,
    ) -> Document:
        """
        Load a document from disk.
        """