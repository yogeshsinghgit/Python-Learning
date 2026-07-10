"""
Base interface for chunk enrichment.
"""

from abc import ABC, abstractmethod

from app.schemas.chunk import Chunk


class ChunkEnricher(ABC):
    """Enrich chunks before embedding."""

    @abstractmethod
    async def enrich(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Enrich chunks with additional indexed context.

        Args:
            chunks: Original chunks.

        Returns:
            Enriched chunks.
        """
        raise NotImplementedError