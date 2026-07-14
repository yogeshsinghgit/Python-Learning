from loguru import logger

from app.domains.generation.models import (
    TokenizedContextChunk,
)
from app.rag_services.generation.content_window.interfaces.context_truncator import (
    ContextTruncator
)


class DefaultContextTruncator(ContextTruncator):

    async def truncate(
        self,
        chunks: list[TokenizedContextChunk],
        token_budget: int,
    ) -> list[TokenizedContextChunk]:

        logger.debug(
            f"Context budget: {token_budget}"
        )

        #
        # Highest score first
        #

        ordered_chunks = sorted(
            chunks,
            key=lambda chunk: chunk.chunk.score,
            reverse=True,
        )

        selected: list[TokenizedContextChunk] = []

        total_tokens = 0

        for chunk in ordered_chunks:

            if (
                total_tokens + chunk.token_count
                > token_budget
            ):
                continue

            selected.append(chunk)

            total_tokens += chunk.token_count

        logger.info(
            f"Selected {len(selected)} chunks "
            f"({total_tokens} tokens)"
        )

        return selected