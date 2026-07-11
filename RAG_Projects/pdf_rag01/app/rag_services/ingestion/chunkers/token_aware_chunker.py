"""
Token-aware decorator chunker — Phase 2.

Responsibilities:
- Wrap another Chunker.
- Tokenize every produced chunk.
- Populate token_count metadata.
- Split chunks that exceed max_chunk_tokens using a BaseSplitter.

Phase 2 changes from Phase 1:
- Removed ChunkTooLargeError.
- Oversized chunks are transparently split via self._splitter.
- chunk_index is maintained globally across all output chunks.
"""

from __future__ import annotations

from loguru import logger

from app.core.config import get_settings
from app.rag_services.ingestion.interfaces.chunker import Chunker
from app.rag_services.ingestion.interfaces.token_counter import TokenCounter
from app.rag_services.ingestion.splitters.base_splitter import BaseSplitter
from app.schemas.chunk.chunk import Chunk
from app.schemas.document import Document


class TokenAwareChunker(Chunker):
    """
    Decorator chunker that validates and splits chunks by token count.
    """

    def __init__(
        self,
        chunker: Chunker,
        token_counter: TokenCounter,
        splitter: BaseSplitter,
    ) -> None:
        self._chunker = chunker
        self._token_counter = token_counter
        self._splitter = splitter
        self._settings = get_settings()

    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        """
        Generate chunks, then split any that exceed the token limit.
        """

        logger.info(
            f"Running token-aware chunking for '{document.filename}'."
        )

        chunks = await self._chunker.chunk(document)

        processed_chunks: list[Chunk] = []

        chunk_index = 0

        for chunk in chunks:

            processed_chunks.extend(
                self._split_chunk(chunk, chunk_index)
            )

            chunk_index = len(processed_chunks)

        logger.info(
            f"Token-aware chunking completed: "
            f"{len(chunks)} → {len(processed_chunks)} chunks."
        )

        return processed_chunks

    def _split_chunk(
        self,
        chunk: Chunk,
        chunk_index: int,
    ) -> list[Chunk]:
        """
        Tokenize a chunk and split it if it exceeds the token limit.

        Returns a list containing either:
        - The original chunk (with token_count populated), or
        - Multiple sub-chunks produced by the splitter.
        """

        text = chunk.indexed_text or chunk.text

        tokenization = self._token_counter.tokenize(text)

        logger.debug(
            f"Chunk '{chunk.chunk_id}' "
            f"contains {tokenization.token_count} tokens."
        )

        settings = self._settings

        if tokenization.token_count <= settings.max_chunk_tokens:
            # Chunk is within limit — just populate token_count metadata.
            return [
                chunk.model_copy(
                    update={
                        "metadata": chunk.metadata.model_copy(
                            update={
                                "token_count": tokenization.token_count,
                            }
                        )
                    }
                )
            ]

        logger.warning(
            f"Chunk '{chunk.chunk_id}' exceeds limit "
            f"({tokenization.token_count} > "
            f"{settings.max_chunk_tokens} tokens). Splitting."
        )

        return self._splitter.split(
            chunk=chunk,
            tokenization=tokenization,
            chunk_index=chunk_index,
        )