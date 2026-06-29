from typing import Any, Optional

from pydantic import BaseModel, Field
from qdrant_client.http.models import Filter, SparseVector


class SearchQuery(BaseModel):
    dense_vector: list[float] | None = None
    sparse_vector: SparseVector | None = None
    top_k: int = 5
    score_threshold: float | None = None
    metadata_filter: Optional[Filter] = None