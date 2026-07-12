"""
Dependency providers for embedding models.
"""

from functools import lru_cache

from app.infrastructure.embeddings.dense.sentence_transformer import (
    SentenceTransformerDenseEmbedder,
)
from app.infrastructure.embeddings.sparse.fastembed_sparse import (
    FastEmbedSparseEmbedder,
)



from dataclasses import dataclass

from app.infrastructure.vector_db.base import VectorStoreRepository
from app.infrastructure.embeddings.interfaces.dense_embedder import DenseEmbedder
from app.infrastructure.embeddings.interfaces.sparse_embedder import SparseEmbedder


@dataclass
class AppState:
    dense_embedder: DenseEmbedder | None = None
    sparse_embedder: SparseEmbedder | None = None
    vector_repository: VectorStoreRepository | None = None

    # Future
    # cross_encoder: CrossEncoder | None = None
    # llm_client: LLMClient | None = None

state = AppState()


def get_dense_embedder() -> DenseEmbedder:
    if state.dense_embedder is None:
        raise RuntimeError("Dense embedder has not been initialized.")
    return state.dense_embedder


def get_sparse_embedder() -> SparseEmbedder:
    if state.sparse_embedder is None:
        raise RuntimeError("Sparse embedder has not been initialized.")
    return state.sparse_embedder


def get_vector_repository() -> VectorStoreRepository:
    if state.vector_repository is None:
        raise RuntimeError("Vector repository has not been initialized.")
    return state.vector_repository

# @lru_cache
# def get_dense_embedder() -> SentenceTransformerDenseEmbedder:
#     """
#     Return a singleton dense embedder.
#     """
#     return SentenceTransformerDenseEmbedder()


# @lru_cache
# def get_sparse_embedder() -> FastEmbedSparseEmbedder:
#     """
#     Return a singleton sparse embedder.
#     """
#     return FastEmbedSparseEmbedder()