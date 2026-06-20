from loguru import logger

from app.services.document_loader import (
    DocumentLoader,
)

from app.services.chunking_service import (
    ChunkingService,
)

from app.services.embedding_service import (
    EmbeddingService,
)

from app.repositories.qdrant_repository import (
    QdrantRepository,
)


class IngestionService:

    def __init__(self) -> None:

        self._loader = DocumentLoader()

        self._chunker = ChunkingService(chunk_size=100, chunk_overlap=20)

        self._embedder = EmbeddingService()

        self._repository = (
            QdrantRepository()
        )

    async def ingest(
        self,
        docs_path: str,
    ) -> None:

        await self._repository.create_collection()

        documents = (
            await self._loader.load_documents(
                docs_path
            )
        )

        for document in documents:

            chunks = (
                await self._chunker.create_chunks(
                    document
                )
            )

            for chunk in chunks:

                embedded_chunk = (
                    await self._embedder
                    .generate_embedding(chunk)
                )

                await self._repository.insert_chunk(
                    embedded_chunk
                )

        logger.info(
            "Ingestion completed"
        )