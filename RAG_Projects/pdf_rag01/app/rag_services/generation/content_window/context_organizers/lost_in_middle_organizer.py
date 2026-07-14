from loguru import logger

from app.domains.generation.models import (
    TokenizedContextChunk,
)
from app.rag_services.generation.content_window.interfaces.context_organizer import (
    ContextOrganizer
)


class LostMiddleContextOrganizer(ContextOrganizer):

    async def organize(
        self,
        chunks: list[TokenizedContextChunk],
    ) -> list[TokenizedContextChunk]:

        if len(chunks) <= 2:
            return chunks

        ordered = sorted(
            chunks,
            key=lambda chunk: chunk.chunk.score,
            reverse=True,
        )

        front: list[TokenizedContextChunk] = []
        back: list[TokenizedContextChunk] = []

        for index, chunk in enumerate(ordered):

            if index % 2 == 0:
                front.append(chunk)
            else:
                back.insert(0, chunk)

        organized = front + back

        logger.debug(
            f"Applied Lost-In-The-Middle mitigation "
            f"to {len(chunks)} chunks."
        )

        return organized