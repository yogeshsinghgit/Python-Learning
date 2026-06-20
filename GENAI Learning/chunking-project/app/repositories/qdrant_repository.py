from uuid import uuid4

from loguru import logger

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import settings
from app.schemas.embedded_chunk import (
    EmbeddedChunk,
)


class QdrantRepository:

    def __init__(self) -> None:

        self._client = QdrantClient(
            url=settings.qdrant_url
        )

    async def create_collection(
        self,
    ) -> None:

        try:

            collections = (
                self._client
                .get_collections()
            )

            existing = {
                collection.name
                for collection
                in collections.collections
            }

            if settings.collection_name in existing:

                logger.info(
                    "Collection already exists"
                )

                return

            self._client.create_collection(
                collection_name=
                settings.collection_name,

                vectors_config=VectorParams(
                    size=settings.embedding_dimension,
                    distance=Distance.COSINE,
                ),
            )

            logger.info(
                f"Created collection "
                f"{settings.collection_name}"
            )

        except Exception as exc:

            logger.exception(
                f"Collection creation failed: {exc}"
            )

            raise

    async def insert_chunk(
        self,
        chunk: EmbeddedChunk,
    ) -> None:

        try:

            point = PointStruct(
                id=str(uuid4()),

                vector=chunk.vector,

                payload={
                    "chunk_id": chunk.chunk_id,
                    "document_id":
                        chunk.document_id,
                    "chunk_index":
                        chunk.chunk_index,
                    "content":
                        chunk.content,
                },
            )

            self._client.upsert(
                collection_name=
                settings.collection_name,

                points=[point],
            )

            logger.info(
                f"Stored chunk "
                f"{chunk.chunk_id}"
            )

        except Exception as exc:

            logger.exception(
                f"Insert failed: {exc}"
            )

            raise