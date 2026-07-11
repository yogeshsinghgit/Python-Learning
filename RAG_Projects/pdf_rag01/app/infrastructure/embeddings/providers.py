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

from app.infrastructure.embeddings.interfaces.dense_embedder import DenseEmbedder
from app.infrastructure.embeddings.interfaces.sparse_embedder import SparseEmbedder


@dataclass
class AppState:
    dense_embedder: DenseEmbedder
    sparse_embedder: SparseEmbedder


state = AppState(
    dense_embedder=None,
    sparse_embedder=None,
)


def get_dense_embedder() -> DenseEmbedder:
    return state.dense_embedder


def get_sparse_embedder() -> SparseEmbedder:
    return state.sparse_embedder

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