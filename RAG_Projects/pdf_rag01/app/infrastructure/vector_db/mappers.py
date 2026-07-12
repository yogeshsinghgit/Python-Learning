from typing import Any

from app.infrastructure.vector_db.models import (
    QueryResult,
    VectorDocument,
    DenseVector,
    SparseVector
)


def to_pinecone_payload(vector: VectorDocument) -> dict[str, Any]:
    """
    Convert VectorDocument into Pinecone payload.
    """
    payload = {
        "id": vector.id,
        "metadata": vector.metadata,
    }

    if vector.dense_vector:
        payload["values"] = vector.dense_vector.values

    if vector.sparse_vector:
        payload["sparse_values"] = {
            "indices": vector.sparse_vector.indices,
            "values": vector.sparse_vector.values,
        }

    return payload


def to_query_result(match: Any) -> QueryResult:
    """
    Convert Pinecone match into QueryResult.
    """
    metadata = match.metadata or {}
    return QueryResult(
        id=match.id,
        score=match.score,
        text=metadata.get("text", ""),
        metadata=metadata,
        dense_vector=DenseVector(values=match.values) if hasattr(match, 'values') and match.values else None,
        sparse_vector=SparseVector(indices=match.sparse_values.indices, values=match.sparse_values.values) if hasattr(match, 'sparse_values') and match.sparse_values else None,
    )


def to_vector_document(match: Any) -> VectorDocument:
    """
    Convert Pinecone match into VectorDocument.
    """
    return VectorDocument(
        id=match.id,
        metadata=match.metadata or {},
        dense_vector=DenseVector(values=match.values) if hasattr(match, 'values') and match.values else None,
        sparse_vector=SparseVector(indices=match.sparse_values.indices, values=match.sparse_values.values) if hasattr(match, 'sparse_values') and match.sparse_values else None,
    )
