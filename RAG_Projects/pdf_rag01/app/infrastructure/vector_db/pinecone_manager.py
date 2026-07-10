"""
Pinecone Index Manager.

Responsibilities:
- Create index
- Delete index
- Check index existence
- Wait until index becomes ready
- Describe index
- List indexes

NOTE:
This class manages ONLY the lifecycle of a Pinecone index.

It does NOT perform CRUD operations on vectors.
"""

from __future__ import annotations

import asyncio

from loguru import logger
from pinecone import ServerlessSpec

from app.core.config import get_settings
from app.core.exceptions import VectorStoreError
from app.infrastructure.vector_db.pinecone_client import PineconeClient, get_pinecone_client


class PineconeManager:
    """
    Manages the lifecycle of a Pinecone Index.
    """

    def __init__(self) -> None:
        self._settings = get_settings()
        self._client = get_pinecone_client().client

    async def index_exists(self) -> bool:
        """
        Check whether the configured index already exists.
        """

        try:
            logger.info(
                f"Checking if Pinecone index '{self._settings.pinecone_index_name}' exists."
            )

            indexes = self._client.list_indexes().names()

            exists = self._settings.pinecone_index_name in indexes

            logger.info(
                f"Pinecone index exists: {exists}"
            )

            return exists

        except Exception as exc:
            logger.exception(
                f"Failed to check Pinecone index existence: {exc}"
            )
            raise VectorStoreError(
                "Unable to check Pinecone index."
            ) from exc

    async def create_index(self) -> None:
        """
        Create the Pinecone index if it does not already exist.
        """

        try:

            if await self.index_exists():
                logger.info(
                    f"Pinecone index '{self._settings.pinecone_index_name}' already exists."
                )
                return

            logger.info(
                f"Creating Pinecone index '{self._settings.pinecone_index_name}'."
            )

            # dimension = await dense_embedder.dimension()

            self._client.create_index(
                name=self._settings.pinecone_index_name,
                dimension=self._settings.embedding_dimension,
                metric=self._settings.similarity_metric,
                spec=ServerlessSpec(
                    cloud=self._settings.pinecone_cloud,
                    region=self._settings.pinecone_region,
                ),
            )

            logger.success(
                f"Pinecone index '{self._settings.pinecone_index_name}' created successfully."
            )

        except Exception as exc:
            logger.exception(
                f"Failed to create Pinecone index: {exc}"
            )
            raise VectorStoreError(
                "Unable to create Pinecone index."
            ) from exc

    async def wait_until_ready(
        self,
        polling_interval: int = 2,
    ) -> None:
        """
        Wait until the Pinecone index becomes ready.
        """

        logger.info(
            f"Waiting for Pinecone index '{self._settings.pinecone_index_name}' to become ready."
        )

        while True:

            try:

                description = self._client.describe_index(
                    self._settings.pinecone_index_name
                )

                if description.status.ready:
                    logger.success(
                        f"Pinecone index '{self._settings.pinecone_index_name}' is ready."
                    )
                    return

                logger.info(
                    "Index is still initializing..."
                )

                await asyncio.sleep(polling_interval)

            except Exception as exc:
                logger.exception(
                    f"Failed while waiting for index readiness: {exc}"
                )
                raise VectorStoreError(
                    "Error waiting for Pinecone index."
                ) from exc

    async def delete_index(self) -> None:
        """
        Delete the configured Pinecone index.
        """

        try:

            if not await self.index_exists():

                logger.warning(
                    f"Pinecone index '{self._settings.pinecone_index_name}' does not exist."
                )
                return

            logger.warning(
                f"Deleting Pinecone index '{self._settings.pinecone_index_name}'."
            )

            self._client.delete_index(
                self._settings.pinecone_index_name
            )

            logger.success(
                f"Pinecone index '{self._settings.pinecone_index_name}' deleted successfully."
            )

        except Exception as exc:
            logger.exception(
                f"Failed to delete Pinecone index: {exc}"
            )
            raise VectorStoreError(
                "Unable to delete Pinecone index."
            ) from exc

    async def describe_index(self):
        """
        Return the index description.
        """

        try:

            logger.info(
                f"Fetching description for '{self._settings.pinecone_index_name}'."
            )

            return self._client.describe_index(
                self._settings.pinecone_index_name
            )

        except Exception as exc:
            logger.exception(
                f"Failed to describe Pinecone index: {exc}"
            )
            raise VectorStoreError(
                "Unable to describe Pinecone index."
            ) from exc

    async def list_indexes(self) -> list[str]:
        """
        Return all indexes available in the Pinecone project.
        """

        try:

            logger.info("Listing Pinecone indexes.")

            indexes = self._client.list_indexes().names()

            logger.info(
                f"Found {len(indexes)} Pinecone indexes."
            )

            return indexes

        except Exception as exc:
            logger.exception(
                f"Failed to list Pinecone indexes: {exc}"
            )
            raise VectorStoreError(
                "Unable to list Pinecone indexes."
            ) from exc