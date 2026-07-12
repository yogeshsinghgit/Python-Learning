
from fastapi import Depends

from app.rag_services.retrieval.interfaces.query_preprocessor import (
    QueryPreprocessor,
)
from app.rag_services.retrieval.preprocessors.default_query_preprocessor import (
    DefaultQueryPreprocessor,
)

from app.infrastructure.vector_db.pinecone_repository import VectorStoreRepository

from app.infrastructure.embeddings.providers import get_dense_embedder, get_sparse_embedder

from app.infrastructure.embeddings.interfaces.dense_embedder import DenseEmbedder
from app.infrastructure.embeddings.interfaces.sparse_embedder import SparseEmbedder

from app.rag_services.retrieval.builders.query_vector_builder import (
    QueryVectorBuilder,
)

from app.rag_services.retrieval.pipeline.retrieval_pipeline import RetrievalPipeline

from app.rag_services.retrieval.mappers.retrieval_result_mapper import (
    RetrievalResultMapper,
)



def get_query_preprocessor() -> QueryPreprocessor:
    """
    Returns the default query preprocessor implementation.
    """
    return DefaultQueryPreprocessor()


def get_query_vector_builder(
    dense_embedder: DenseEmbedder = Depends(get_dense_embedder),
    sparse_embedder: SparseEmbedder = Depends(get_sparse_embedder),
) -> QueryVectorBuilder:

    return QueryVectorBuilder(
        dense_embedder=dense_embedder,
        sparse_embedder=sparse_embedder,
    )


def get_retrieval_pipeline(
    query_preprocessor: QueryPreprocessor = Depends(
        get_query_preprocessor
    ),
    query_vector_builder: QueryVectorBuilder = Depends(
        get_query_vector_builder
    ),
    vector_repository: VectorStoreRepository = Depends(
        get_vector_repository
    ),
) -> RetrievalPipeline:

    return RetrievalPipeline(
        query_preprocessor=query_preprocessor,
        query_vector_builder=query_vector_builder,
        vector_repository=vector_repository,
    )


def get_retrieval_result_mapper() -> RetrievalResultMapper:
    return RetrievalResultMapper()