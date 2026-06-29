from qdrant_client import AsyncQdrantClient

from core.config import get_settings
from ingestion.sentence_transformers.dense_embedder import SentenceTransformerDenseEmbedder
from ingestion.fastembed.sparse_embedder import FastEmbedSparseEmbedder
from retrieval.qdrant.qdrant_search_repository import QdrantSearchRepository
from retrieval.services.rrf_service import RRFService
from retrieval.services.retrieval_service import RetrievalService


def get_retrieval_service() -> RetrievalService:
    """
    Build the RetrievalService and all of its dependencies.
    """

    settings = get_settings()

    client = AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
    )

    repository = QdrantSearchRepository(
        client=client,
        collection_name=settings.qdrant_collection,
    )

    dense_embedder = SentenceTransformerDenseEmbedder(model_name=settings.dense_model)
    sparse_embedder = FastEmbedSparseEmbedder(model_name=settings.sparse_model)

    return RetrievalService(
        dense_embedder=dense_embedder,
        sparse_embedder=sparse_embedder,
        search_repository=repository,
        rrf_service=RRFService(),
    )