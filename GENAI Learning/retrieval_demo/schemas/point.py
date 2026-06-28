from typing import Any

from pydantic import BaseModel, Field

from schemas.vectors import (
    DenseVector,
    SparseVectorData,
)


class HybridPoint(BaseModel):
    point_id: str
    dense: DenseVector
    sparse: SparseVectorData
    payload: dict[str, Any] = Field(
        default_factory=dict
    )