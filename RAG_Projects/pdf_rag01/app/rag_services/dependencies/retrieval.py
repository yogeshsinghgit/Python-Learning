from app.rag_services.retrieval.interfaces.query_preprocessor import (
    QueryPreprocessor,
)
from app.rag_services.retrieval.preprocessors.default_query_preprocessor import (
    DefaultQueryPreprocessor,
)


def get_query_preprocessor() -> QueryPreprocessor:
    """
    Returns the default query preprocessor implementation.
    """
    return DefaultQueryPreprocessor()