"""
Application-wide custom exceptions.

Purpose:
- Define a common exception hierarchy for the application.
- Allow catching application-specific errors instead of generic Exception.
- Provide meaningful error messages for debugging and API responses.

All custom exceptions should inherit from `ApplicationError`.
"""


class ApplicationError(Exception):
    """
    Base class for all custom application exceptions.

    Every application-specific exception should inherit from this class.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


# --------------------------------------------------------------------------
# Configuration Exceptions
# --------------------------------------------------------------------------


class ConfigurationError(ApplicationError):
    """
    Raised when the application configuration is invalid.

    Examples:
    - Missing environment variables.
    - Invalid configuration values.
    - Unsupported deployment settings.
    """


# --------------------------------------------------------------------------
# Vector Database Exceptions
# --------------------------------------------------------------------------


class VectorStoreError(ApplicationError):
    """
    Raised when a vector database operation fails.

    Examples:
    - Connection failure.
    - Index creation failure.
    - Upsert failure.
    - Query failure.
    """


# --------------------------------------------------------------------------
# Embedding Exceptions
# --------------------------------------------------------------------------


class EmbeddingError(ApplicationError):
    """
    Raised when embedding generation fails.

    Examples:
    - Embedding model unavailable.
    - Invalid input.
    - Provider/API failure.
    """


# --------------------------------------------------------------------------
# Retrieval Exceptions
# --------------------------------------------------------------------------


class RetrievalError(ApplicationError):
    """
    Raised when document retrieval fails.

    Examples:
    - Similarity search failure.
    - Metadata filter failure.
    - Empty retrieval when documents are expected.
    """


# --------------------------------------------------------------------------
# Generation / LLM Exceptions
# --------------------------------------------------------------------------


class LLMError(ApplicationError):
    """
    Raised when an LLM request fails.

    Examples:
    - API timeout.
    - Invalid response.
    - Authentication failure.
    - Rate limiting.
    """


# --------------------------------------------------------------------------
# Document Processing Exceptions
# --------------------------------------------------------------------------


class DocumentProcessingError(ApplicationError):
    """
    Raised when document ingestion or parsing fails.

    Examples:
    - PDF parsing failure.
    - Corrupted document.
    - Unsupported file format.
    """


# --------------------------------------------------------------------------
# Validation Exceptions
# --------------------------------------------------------------------------


class ValidationError(ApplicationError):
    """
    Raised when business validation fails.

    Examples:
    - Empty question.
    - Invalid metadata.
    - Unsupported request.
    """

class DocumentLoadingError(Exception):
    """
    Raised when a document cannot be loaded.
    - wrong path
    - invalid document type
    - invalid document
    """