"""
Token-window chunk splitter.

Splits an oversized chunk into fixed-size token windows with overlap.

Algorithm:
    step = max_chunk_tokens - chunk_overlap_tokens

    For every window [start : start + max_chunk_tokens]:
        1. Decode token ids back to text.
        2. Build a sub-chunk via ChunkMapper.from_existing_chunk().
        3. Advance start by step.

This produces sub-chunks that each share `chunk_overlap_tokens` tokens
with the following window, preserving retrieval context across boundaries.
"""

from __future__ import annotations

from loguru import logger

from app.core.config import get_settings
from app.rag_services.ingestion.interfaces.token_counter import TokenCounter
from app.rag_services.ingestion.mappers.chunk_mapper import ChunkMapper
from app.rag_services.ingestion.splitters.base_splitter import BaseSplitter
from app.rag_services.ingestion.tokenizers.models import TokenizationResult
from app.schemas.chunk.chunk import Chunk


class TokenSplitter(BaseSplitter):
    """
    Splits a chunk into overlapping token windows.
    """

    def __init__(
        self,
        token_counter: TokenCounter,
    ) -> None:
        self._token_counter = token_counter
        self._settings = get_settings()

    def split(
        self,
        *,
        chunk: Chunk,
        tokenization: TokenizationResult,
        chunk_index: int,
    ) -> list[Chunk]:
        """
        Split an oversized chunk into token-window sub-chunks.
        """

        settings = self._settings

        max_tokens = settings.max_chunk_tokens
        overlap = settings.chunk_overlap_tokens
        step = max_tokens - overlap

        token_ids = tokenization.token_ids
        chunks: list[Chunk] = []
        current_index = chunk_index

        for start in range(0, len(token_ids), step):

            end = start + max_tokens
            window = token_ids[start:end]
            text = self._token_counter.decode(window)

            logger.debug(
                f"Splitting chunk '{chunk.chunk_id}': "
                f"window [{start}:{end}], {len(window)} tokens."
            )

            chunks.append(
                ChunkMapper.from_existing_chunk(
                    chunk=chunk,
                    text=text,
                    chunk_index=current_index,
                    token_count=len(window),
                )
            )

            current_index += 1

        return chunks
