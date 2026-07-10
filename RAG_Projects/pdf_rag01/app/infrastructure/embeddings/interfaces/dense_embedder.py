"""
Abstract interface for dense embedding providers.
"""

from abc import ABC, abstractmethod

from app.infrastructure.vector_db.models import DenseVector


class DenseEmbedder(ABC):
    """
    Base interface for all dense embedding providers.
    """

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> DenseVector:
        """
        Generate embedding for a single text.
        """

    @abstractmethod
    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[DenseVector]:
        """
        Generate embeddings for multiple texts.
        """

    @abstractmethod
    async def dimension(self) -> int:
        """
        Return embedding dimension.
        """