"""
Abstract interface for sparse embedding providers.
"""

from abc import ABC, abstractmethod

from app.infrastructure.vector_db.models import SparseVector


class SparseEmbedder(ABC):
    """
    Base interface for sparse embedding providers.
    """

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> SparseVector:
        """
        Generate sparse embedding for a single text.
        """

    @abstractmethod
    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[SparseVector]:
        """
        Generate sparse embeddings for multiple texts.
        """