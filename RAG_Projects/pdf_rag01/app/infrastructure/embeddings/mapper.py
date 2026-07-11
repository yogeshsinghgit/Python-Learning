"""
Embedding mappers.
"""

from app.infrastructure.vector_db.models import (
    DenseVector,
    SparseVector,
    VectorDocument,
)
from app.schemas.chunk.chunk import Chunk


def create_vector_document(
    chunk: Chunk,
    dense_vector: DenseVector,
    sparse_vector: SparseVector,
) -> VectorDocument:
    """
    Convert a Chunk and its embeddings into a VectorDocument.
    """

    return VectorDocument(
        id=chunk.chunk_id,
        dense_vector=dense_vector,
        sparse_vector=sparse_vector,
        metadata={
            "document_id": chunk.document_id,
            "text": chunk.text,
            **chunk.metadata.model_dump(exclude_none=True),
        },
    )