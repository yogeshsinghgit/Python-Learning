from loguru import logger

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    SparseVectorParams,
    VectorParams,
)

from exceptions.collection import (
    CollectionCreationError,
    CollectionNotFoundError,
)
from exceptions.connection import VectorDatabaseConnectionError
from repositories.interfaces.collection_repository import (
    CollectionRepository,
)


class QdrantCollectionRepository(CollectionRepository):

    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str,
        dense_vector_size: int
    ) -> None:
        self._client = client
        self._collection_name = collection_name
        self._dense_vector_size = dense_vector_size

    async def verify_connection(self) -> None:
        """
        Verify the connection to the Qdrant server.
        """
        try:
            await self._client.get_collections()
            logger.info("Qdrant connection verified.")
        except Exception as exc:
            logger.exception(
                f"Failed to connect to Qdrant: {exc}"
            )
            raise VectorDatabaseConnectionError(
                "Unable to reach Qdrant."
            ) from exc

    async def collection_exists(self) -> bool:
        """
        Check whether the configured collection exists.
        """
        try:
            exists = await self._client.collection_exists(
                collection_name=self._collection_name,
            )

            logger.info(
                f"Collection '{self._collection_name}' exists: {exists}"
            )

            return exists

        except Exception as exc:
            logger.exception(
                f"Failed checking collection: {exc}"
            )
            raise CollectionCreationError(
                "Unable to determine collection status."
            ) from exc

    async def create_collection(self) -> None:
        """
        Create the Hybrid Search collection.
        """

        try:

            if await self.collection_exists():
                logger.info(
                    f"Collection '{self._collection_name}' already exists."
                )
                return

            logger.info(
                f"Creating collection '{self._collection_name}'..."
            )

            await self._client.create_collection(
                collection_name=self._collection_name,
                vectors_config={
                    "dense": VectorParams(
                        size=self._dense_vector_size,
                        distance=Distance.COSINE,
                    ),
                },
                sparse_vectors_config={
                    "sparse": SparseVectorParams(),
                },
            )

            logger.success(
                f"Collection '{self._collection_name}' created successfully."
            )

        except Exception as exc:
            logger.exception(
                f"Collection creation failed: {exc}"
            )

            raise CollectionCreationError(
                f"Failed creating '{self._collection_name}'."
            ) from exc

    async def delete_collection(self) -> None:
        """
        Delete the configured collection.
        """

        try:

            if not await self.collection_exists():
                logger.warning(
                    f"Collection '{self._collection_name}' does not exist."
                )
                return

            logger.info(
                f"Deleting collection '{self._collection_name}'..."
            )

            await self._client.delete_collection(
                collection_name=self._collection_name,
            )

            logger.success(
                f"Collection '{self._collection_name}' deleted."
            )

        except Exception as exc:
            logger.exception(
                f"Failed deleting collection: {exc}"
            )

            raise CollectionNotFoundError(
                f"Failed deleting '{self._collection_name}'."
            ) from exc

    async def close(self) -> None:
        """
        Close the Qdrant async client connection.
        """
        await self._client.close()
        logger.info("Qdrant client connection closed.")