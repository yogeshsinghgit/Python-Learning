import sys
from pathlib import Path
# Add the parent directory of 'app' to the search path
sys.path.append(str(Path(__file__).resolve().parent.parent))
# run code using : python -m app.main

import asyncio

from app.services.chunking_service import (
    ChunkingService,
)
from app.services.document_loader import (
    DocumentLoader,
)

from app.services.embedding_service import (
    EmbeddingService
)
from app.services.ingestion_service import (
    IngestionService
)


# Project root is the parent of the 'app' directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


async def main() -> None:

    # loader = DocumentLoader()

    # documents = await loader.load_documents(
    #     docs_path=str(PROJECT_ROOT / "docs"),
    # )

    # chunk_service = ChunkingService(
    #     chunk_size=100,
    #     chunk_overlap=20,
    # )
    # embedding_service = EmbeddingService()

    # for document in documents:

    #     chunks = await chunk_service.create_chunks(
    #         document
    #     )

    #     for chunk in chunks:

    #         embedded_chunk = (
    #             await embedding_service
    #             .generate_embedding(chunk)
    #         )

    #         print(
    #             f"Chunk Index: "
    #             f"{embedded_chunk.chunk_index}"
    #         )

    #         print(
    #             f"Vector Dimension: "
    #             f"{len(embedded_chunk.vector)}"
    #         )

    #         print(
    #             f"First 5 Values: "
    #             f"{embedded_chunk.vector[:5]}"
    #         )

    #         print("-" * 80)
    service = IngestionService()

    await service.ingest(
        docs_path=str(PROJECT_ROOT / "docs")
    )


if __name__ == "__main__":
    asyncio.run(main())