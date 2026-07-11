"""
Default chunk enricher.

Currently this implementation performs no enrichment and simply
ensures every chunk has indexed_text populated.
"""

from loguru import logger

from app.rag_services.ingestion.interfaces.chunk_enricher import ChunkEnricher
from app.schemas.chunk.chunk import Chunk


class DefaultChunkEnricher(ChunkEnricher):
    """Default implementation."""

    async def enrich(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        logger.info(
            f"Enriching {len(chunks)} chunks."
        )

        enriched_chunks: list[Chunk] = []

        for chunk in chunks:

            enriched_chunks.append(
                chunk.model_copy(
                    update={
                        "indexed_text": chunk.indexed_text or chunk.text,
                    }
                )
            )

        logger.info(
            f"Successfully enriched {len(enriched_chunks)} chunks."
        )

        return enriched_chunks