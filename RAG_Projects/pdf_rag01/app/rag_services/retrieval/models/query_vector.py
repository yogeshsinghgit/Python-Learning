from pydantic import BaseModel

from app.infrastructure.vector_db.models import DenseVector, SparseVector

class QueryVector(BaseModel):
    """
    Represents the vectorized form of a query.

    This model is provider-independent and is consumed by
    the retrieval pipeline.
    """
    dense: DenseVector
    sparse: SparseVector