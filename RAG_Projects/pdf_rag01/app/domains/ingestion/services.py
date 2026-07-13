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

from app.rag_services.ingestion.filters.document_filter_pipeline import DefaultDocumentFilterPipeline
from app.rag_services.ingestion.filters.blank_element_filter import BlankElementFilter
from app.rag_services.ingestion.filters.header_footer_filter import HeaderFooterFilter
from app.rag_services.ingestion.filters.front_matter_filter import FrontMatterFilter 
from app.rag_services.ingestion.filters.page_number_filter import PageNumberFilter
from app.rag_services.ingestion.filters.table_of_content_filter import TableOfContentsFilter 
from app.infrastructure.vector_db.pinecone_repository import (
    PineconeRepository,
)





def get_document_ingestion_pipeline() -> DocumentIngestionPipeline:
    """
    Dependency provider.
    """

    token_counter = TiktokenTokenCounter()

    filter_pipeline = DefaultDocumentFilterPipeline(
    filters=[
                BlankElementFilter(),
                HeaderFooterFilter(),
                PageNumberFilter(),
                TableOfContentsFilter(),
                FrontMatterFilter(),
                # BoilerplateRepetitionFilter(),
            ]
        )

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
        filter_pipeline=filter_pipeline,
        chunker=chunker,
        enricher=DefaultChunkEnricher(),
        vector_document_builder=VectorDocumentBuilder(
            dense_embedder=get_dense_embedder(),
            sparse_embedder=get_sparse_embedder(),
        ),
        repository=PineconeRepository(),
    )