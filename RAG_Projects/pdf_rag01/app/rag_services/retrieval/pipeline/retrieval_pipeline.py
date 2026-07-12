import time

from loguru import logger

from app.infrastructure.vector_db.pinecone_repository import VectorStoreRepository

from app.rag_services.retrieval.builders.query_vector_builder import (
    QueryVectorBuilder,
)
from app.rag_services.retrieval.interfaces.query_preprocessor import (
    QueryPreprocessor,
)
from app.rag_services.retrieval.models.retrieval_request import (
    RetrievalRequest,
)
from app.rag_services.retrieval.models.retrieval_result import (
    RetrievalResult,
)
from app.rag_services.retrieval.models.llm_context import (
    LLMContext
)

from app.rag_services.retrieval.mappers.retrieval_result_mapper import RetrievalResultMapper

from app.rag_services.retrieval.interfaces.reranker import Reranker
from app.rag_services.retrieval.interfaces.context_builder import ContextBuilder

class RetrievalPipeline:
    """
    Orchestrates the complete document retrieval process.

    Responsibilities:
        - Normalize the query
        - Generate query embeddings
        - Query the vector database
        - Convert repository models into retrieval models
    """

    def __init__(
        self,
        query_preprocessor: QueryPreprocessor,
        query_vector_builder: QueryVectorBuilder,
        vector_repository: VectorStoreRepository,
        retrieval_result_mapper: RetrievalResultMapper,
        reranker: Reranker,
        context_builder: ContextBuilder,
    ) -> None:
        self._query_preprocessor = query_preprocessor
        self._query_vector_builder = query_vector_builder
        self._vector_repository = vector_repository
        self._retrieval_result_mapper = retrieval_result_mapper
        self._reranker = reranker
        self._context_builder = context_builder

    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> LLMContext:

        logger.info(
            f"Starting retrieval for query: '{request.query}'"
        )

        started_at = time.perf_counter()

        try:

            # --------------------------------------------------
            # Step 1 : Normalize query
            # --------------------------------------------------

            normalized_query = await self._query_preprocessor.preprocess(
                request.query
            )

            logger.debug(
                f"Normalized query: '{normalized_query}'"
            )

            # --------------------------------------------------
            # Step 2 : Generate query vectors
            # --------------------------------------------------

            query_vector = await self._query_vector_builder.build(
                normalized_query
            )

            # --------------------------------------------------
            # Step 3 : Query vector database
            # --------------------------------------------------

            query_results = await self._vector_repository.query(
                vector= query_vector,
                top_k=request.top_k,
                namespace=request.namespace,
                metadata_filter=request.metadata_filter,
            )

            logger.info(
                f"Retrieved {len(query_results)} chunks from vector database."
            )

            retrieval_results = self._retrieval_result_mapper.map_many(
                query_results
            )


            logger.info(
                f"Retrieved {len(retrieval_results)} chunks before reranking."
            )

            elapsed = time.perf_counter() - started_at
            logger.success(
                f"Retrieval completed successfully in "
                f"{elapsed:.3f} seconds."
            )

            reranked_results = await self._reranker.rerank(
                query=normalized_query,
                results=retrieval_results,
            )

            logger.success(
                f"Returning {len(reranked_results)} chunks after reranking."
            )

        
            llm_context = await self._context_builder.build(
                reranked_results
            )

            return llm_context

        except Exception as exc:
            logger.exception(
                f"Retrieval pipeline failed: {exc}"
            )
            raise