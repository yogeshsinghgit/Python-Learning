from collections.abc import Iterable

from loguru import logger

from retrieval.models.retrieved_chunk import RetrievedChunk
from generation.models.context import ContextModel

class ContextBuilder:
    """Builds an LLM-ready context from retrieved chunks."""

    SEPARATOR = "\n\n" + ("-" * 80) + "\n\n"

    def build(
        self,
        chunks: Iterable[RetrievedChunk],
    ) -> ContextModel:
        """
        Convert retrieved chunks into a formatted context string.

        Args:
            chunks: Retrieved chunks ordered by relevance.

        Returns:
            Formatted context string.
        """

        try:
            unique_chunks: list[RetrievedChunk] = []
            seen_chunk_ids: set[str] = set()

            for chunk in chunks:

                if chunk.chunk_id in seen_chunk_ids:
                    continue

                seen_chunk_ids.add(chunk.chunk_id)
                unique_chunks.append(chunk)

            logger.info(
                f"Building context using {len(unique_chunks)} unique chunks."
            )

            documents: list[str] = []

            for index, chunk in enumerate(unique_chunks, start=1):

                document = (
                    f"[Document {index}]\n\n"
                    f"Source: {chunk.source}\n\n"
                    f"{chunk.content}"
                )

                documents.append(document)

            context = self.SEPARATOR.join(documents)

            logger.info(
                f"Generated context with "
                f"{len(unique_chunks)} chunks "
                f"and {len(context)} characters."
            )

            return ContextModel(
                context=context,
                chunk_count=len(unique_chunks),
                character_count=len(context),
            )

        except Exception as exc:
            logger.exception(
                f"Failed to build context: {exc}"
            )
            raise