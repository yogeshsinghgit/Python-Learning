from app.rag_services.ingestion.pipeline.document_ingestion_pipeline import (
    DocumentIngestionPipeline,
)

# import all implementations
from app.rag_services.ingestion.loaders.unstructured_document_loader import (
    UnstructuredDocumentLoader,
)
from app.rag_services.ingestion.preprocessors.default_document_preprocessor import (
    DefaultDocumentPreprocessor,
)
from app.rag_services.ingestion.chunkers.semantic_element_chunker import (
    SemanticElementChunker,
)

from app.rag_services.ingestion.chunkers.token_aware_chunker import (
    TokenAwareChunker,
)
from app.rag_services.ingestion.enrichers.default_chunk_enricher import (
    DefaultChunkEnricher,
)
from app.rag_services.ingestion.splitters.token_splitter import (
    TokenSplitter,
)
from app.rag_services.ingestion.tokenizers.tiktoken_token_counter import (
    TiktokenTokenCounter,
)
from app.infrastructure.embeddings.vector_document_builder import (
    VectorDocumentBuilder,
)

from app.infrastructure.embeddings.dense.sentence_transformer import SentenceTransformerDenseEmbedder
from app.infrastructure.embeddings.sparse.fastembed_sparse import FastEmbedSparseEmbedder

from app.infrastructure.embeddings.providers import get_dense_embedder, get_sparse_embedder


from app.infrastructure.vector_db.pinecone_repository import (
    PineconeRepository,
)


def get_document_ingestion_pipeline() -> DocumentIngestionPipeline:
    """
    Dependency provider.
    """

    token_counter = TiktokenTokenCounter()

    chunker = TokenAwareChunker(
        chunker=SemanticElementChunker(),
        token_counter=token_counter,
        splitter=TokenSplitter(
            token_counter=token_counter,
        ),
    )

    return DocumentIngestionPipeline(
        loader=UnstructuredDocumentLoader(),
        preprocessor=DefaultDocumentPreprocessor(),
        chunker=chunker,
        enricher=DefaultChunkEnricher(),
        vector_document_builder=VectorDocumentBuilder(
            dense_embedder=get_dense_embedder(),
            sparse_embedder=get_sparse_embedder(),
        ),
        repository=PineconeRepository(),
    )