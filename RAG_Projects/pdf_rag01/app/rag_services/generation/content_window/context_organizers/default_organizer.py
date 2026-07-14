from app.domains.generation.models import TokenizedContextChunk
from app.rag_services.generation.content_window.context_organizers import (
    ContextOrganizer
)

class DefaultContextOrganizer(ContextOrganizer):

    async def organize(
        self,
        chunks: list[TokenizedContextChunk],
    ) -> list[TokenizedContextChunk]:

        return chunks