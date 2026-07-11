"""
Pinecone SDK client.

Responsibilities:
- Initialize the Pinecone SDK.
- Expose the SDK instance.
- Do NOT contain CRUD logic.
"""

from functools import lru_cache

from pinecone import Pinecone

from app.core.config import get_settings


class PineconeClient:
    """
    Wrapper around the Pinecone SDK client.

    This class is responsible only for creating and exposing
    the Pinecone SDK instance.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._client = Pinecone(
            api_key=settings.pinecone_api_key,
        )

    @property
    def client(self) -> Pinecone:
        """
        Return the initialized Pinecone SDK client.
        """
        return self._client


@lru_cache
def get_pinecone_client() -> PineconeClient:
    """
    Return a singleton Pinecone client instance.
    """
    return PineconeClient()