"""
Abstract base class for chunk splitters.

A splitter takes an oversized Chunk and returns a list of smaller Chunks.
It does not decide WHEN to split — that responsibility belongs to the chunker.
"""

from abc import ABC, abstractmethod

from app.rag_services.ingestion.tokenizers.models import TokenizationResult
from app.schemas.chunk.chunk import Chunk


class BaseSplitter(ABC):
    """
    Abstract interface for chunk splitting strategies.
    """

    @abstractmethod
    def split(
        self,
        *,
        chunk: Chunk,
        tokenization: TokenizationResult,
        chunk_index: int,
    ) -> list[Chunk]:
        """
        Split an oversized chunk into smaller sub-chunks.

        Args:
            chunk:
                The oversized source chunk.

            tokenization:
                Pre-computed tokenization result (token_count + token_ids).

            chunk_index:
                Starting index for the first produced sub-chunk.

        Returns:
            List of sub-chunks. Must not be empty.
        """
        raise NotImplementedError
