"""
Production document ingestion pipeline.

Pipeline:

DocumentLoader
        ↓
DocumentPreprocessor
        ↓
Chunker
        ↓
ChunkEnricher
        ↓
VectorDocumentBuilder
        ↓
VectorRepository
"""

from __future__ import annotations

import time
from pathlib import Path

from loguru import logger

from app.rag_services.ingestion.interfaces.chunk_enricher import ChunkEnricher
from app.rag_services.ingestion.interfaces.chunker import Chunker
from app.rag_services.ingestion.interfaces.document_loader import DocumentLoader
from app.rag_services.ingestion.interfaces.document_preprocessor import (
    DocumentPreprocessor,
)
from app.rag_services.ingestion.interfaces.document_filter_pipeline import DocumentFilterPipeline
from app.rag_services.ingestion.models.ingestion_result import (
    IngestionResult,
)

from app.infrastructure.vector_db.base import VectorStoreRepository

from app.infrastructure.embeddings.vector_document_builder import VectorDocumentBuilder


class DocumentIngestionPipeline:
    """
    Coordinates the complete ingestion workflow.
    """

    def __init__(
        self,
        loader: DocumentLoader,
        preprocessor: DocumentPreprocessor,
        filter_pipeline: DocumentFilterPipeline,
        chunker: Chunker,
        enricher: ChunkEnricher,
        vector_document_builder: VectorDocumentBuilder,
        repository: VectorStoreRepository,
    ) -> None:
        self._loader = loader
        self._preprocessor = preprocessor
        self._chunker = chunker
        self._filter_pipeline = filter_pipeline
        self._enricher = enricher
        self._vector_document_builder = vector_document_builder
        self._repository = repository

    async def ingest(
        self,
        file_path: Path,
    ) -> IngestionResult:
        """
        Execute the complete ingestion pipeline.
        """

        logger.info(
            f"Starting ingestion for '{file_path.name}'."
        )

        start_time = time.perf_counter()

        # Load document
        document = await self._loader.load(file_path)

        # Preprocess
        document = await self._preprocessor.preprocess(
            document,
        )

        # Filter
        document = await self._filter_pipeline.filter(document)

        logger.success("Document filtering completed.")

        # Chunk
        chunks = await self._chunker.chunk(
            document,
        )

        logger.success(f"Document chunks are created")

        # Enrich
        chunks = await self._enricher.enrich(
            chunks,
        )

        logger.success(f"Chuns encher executed")

        # Build vector documents
        vector_documents = (
            await self._vector_document_builder.build_batch(
                chunks,
            )
        )

        logger.success(f"Vector Embeddings generated")

        # Persist
        await self._repository.upsert(
            vector_documents,
        )

        processing_time = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            f"Ingestion completed for '{file_path.name}' "
            f"in {processing_time:.2f} ms."
        )

        return IngestionResult(
            document_id=document.document_id,
            filename=document.filename,
            chunk_count=len(chunks),
            vector_count=len(vector_documents),
            checksum=document.metadata.checksum,
            processing_time_ms=processing_time,
        )