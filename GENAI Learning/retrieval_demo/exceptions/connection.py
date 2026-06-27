from exceptions.base import HybridSearchError


class VectorDatabaseConnectionError(HybridSearchError):
    """Raised when the vector database cannot be reached."""

    pass