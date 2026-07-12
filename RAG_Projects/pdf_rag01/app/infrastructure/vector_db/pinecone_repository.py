"""
Pinecone Repository.

Responsibilities
----------------
- Upsert vectors
- Query vectors
- Fetch vectors
- Delete vectors

This class assumes that the Pinecone index already exists.
"""

from __future__ import annotations

from itertools import batched
from loguru import logger
from pinecone import Index

from app.core.config import get_settings
from app.core.exceptions import VectorStoreError
from app.infrastructure.vector_db.base import VectorStoreRepository
from app.infrastructure.vector_db.models import (
    QueryResult,
    QueryVector,
    VectorDocument,
    UpsertResponse,
    DeleteResponse,
)
from app.infrastructure.vector_db.pinecone_client import get_pinecone_client
from app.infrastructure.vector_db.mappers import to_pinecone_payload, to_query_result, to_vector_document


class PineconeRepository(VectorStoreRepository):
    """
    Repository responsible for all vector CRUD operations.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._index: Index = get_pinecone_client().client.Index(
            settings.pinecone_index_name
        )

        self.DEFAULT_BATCH_SIZE = settings.vector_db_batch_size

        logger.info(
            f"Connected to Pinecone index '{settings.pinecone_index_name}'."
        )

    async def upsert(
        self,
        vectors: list[VectorDocument],
        namespace: str | None = None,
    ) -> UpsertResponse:
        """
        Insert or update vectors.
        """

        try:

            logger.info(
                f"Upserting {len(vectors)} vectors in batches of {self.DEFAULT_BATCH_SIZE}."
            )

            payload = [
                to_pinecone_payload(vector)
                for vector in vectors
            ]

            total_upserted = 0

            for i, batch in enumerate(batched(payload, self.DEFAULT_BATCH_SIZE), 1):
                batch_list = list(batch)
                logger.debug(f"Uploading batch {i} of {len(batch_list)} vectors.")
                response = self._index.upsert(
                    vectors=batch_list,
                    namespace=namespace,
                )
                total_upserted += response.upserted_count

            logger.success(
                f"Successfully upserted {total_upserted} vectors."
            )
            
            return UpsertResponse(upserted_count=total_upserted)

        except Exception as exc:

            logger.exception(
                f"Failed to upsert vectors: {exc}"
            )

            raise VectorStoreError(
                "Unable to upsert vectors."
            ) from exc


    async def query(
        self,
        vector: QueryVector,
        top_k: int = 5,
        namespace: str | None = None,
        metadata_filter: dict | None = None,
    ) -> list[QueryResult]:
        """
        Perform similarity search.
        """

        try:

            logger.info(
                f"Querying Pinecone with top_k={top_k}"
            )

            response = self._index.query(
                vector=(
                    vector.dense.values
                    if vector.dense
                    else None
                ),
                sparse_vector=(
                    {
                        "indices": vector.sparse.indices,
                        "values": vector.sparse.values,
                    }
                    if vector.sparse
                    else None
                ),
                top_k=top_k,
                namespace=namespace,
                filter=metadata_filter,
                include_metadata=True,
                include_values=False,
            )

            results = []

            for match in response.matches:
                results.append(to_query_result(match))

            logger.success(
                f"Retrieved {len(results)} vectors."
            )

            return results

        except Exception as exc:

            logger.exception(
                f"Query failed: {exc}"
            )

            raise VectorStoreError(
                "Unable to query vectors."
            ) from exc

    async def fetch(
        self,
        ids: list[str],
        namespace: str | None = None,
    ) -> list[VectorDocument]:
        """
        Fetch vectors by ids.
        """

        try:

            logger.info(
                f"Fetching {len(ids)} vectors."
            )

            response = self._index.fetch(
                ids=ids,
                namespace=namespace,
            )
            
            return [to_vector_document(match) for match in response.vectors.values()]

        except Exception as exc:

            logger.exception(
                f"Fetch failed: {exc}"
            )

            raise VectorStoreError(
                "Unable to fetch vectors."
            ) from exc

    async def delete(
        self,
        ids: list[str],
        namespace: str | None = None,
    ) -> DeleteResponse:
        """
        Delete vectors by ids.
        """

        try:

            logger.info(
                f"Deleting {len(ids)} vectors."
            )

            self._index.delete(
                ids=ids,
                namespace=namespace,
            )

            logger.success(
                "Vectors deleted successfully."
            )
            
            return DeleteResponse(deleted=True)

        except Exception as exc:

            logger.exception(
                f"Delete failed: {exc}"
            )

            raise VectorStoreError(
                "Unable to delete vectors."
            ) from exc

    async def delete_all(
        self,
        namespace: str | None = None,
    ) -> DeleteResponse:
        """
        Delete all vectors inside a namespace.
        """

        try:

            logger.warning(
                f"Deleting all vectors from namespace '{namespace}'."
            )

            self._index.delete(
                delete_all=True,
                namespace=namespace,
            )

            logger.success(
                "Namespace cleared successfully."
            )
            
            return DeleteResponse(deleted=True)

        except Exception as exc:

            logger.exception(
                f"Delete all failed: {exc}"
            )

            raise VectorStoreError(
                "Unable to delete all vectors."
            ) from exc