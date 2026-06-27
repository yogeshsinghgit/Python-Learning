from exceptions.base import HybridSearchError


class CollectionAlreadyExistsError(HybridSearchError):
    """Raised when attempting to create an existing collection."""

    pass


class CollectionNotFoundError(HybridSearchError):
    """Raised when the collection does not exist."""

    pass


class CollectionCreationError(HybridSearchError):
    """Raised when collection creation fails."""

    pass