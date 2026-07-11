"""
Abstract interface for vector database repositories.

All vector database implementations (Pinecone, Qdrant, Weaviate, etc.)
must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.infrastructure.vector_db.models import (
    VectorDocument, 
    QueryResult, 
    QueryVector,
    UpsertResponse,
    DeleteResponse,
    )


class VectorStoreRepository(ABC):
    """
    Base interface for vector database operations.
    """

    @abstractmethod
    async def upsert(
        self,
        vectors: list[VectorDocument],
        namespace: str | None = None,
    ) -> UpsertResponse:
        """
        Insert or update vectors.
        """

    @abstractmethod
    async def query(
        self,
        vector: list[QueryVector],
        top_k: int = 5,
        namespace: str | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[QueryResult]:
        """
        Search similar vectors.
        """

    @abstractmethod
    async def delete(
        self,
        ids: list[str],
        namespace: str | None = None,
    ) -> DeleteResponse:
        """
        Delete vectors by ids.
        """

    @abstractmethod
    async def delete_all(
        self,
        namespace: str | None = None,
    ) -> DeleteResponse:
        """
        Delete all vectors inside a namespace.
        """

    @abstractmethod
    async def fetch(
        self,
        ids: list[str],
        namespace: str | None = None,
    ) -> list[VectorDocument]:
        """
        Fetch vectors by ids.
        """