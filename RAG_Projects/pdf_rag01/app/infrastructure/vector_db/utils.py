from app.infrastructure.vector_db.models import VectorDocument

def _build_vector_payload(
    self,
    vector: VectorDocument,
) -> dict:
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