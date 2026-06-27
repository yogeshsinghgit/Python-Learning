from typing import Any

from pydantic import BaseModel, Field


class HybridPoint(BaseModel):
    point_id: str

    dense_vector: list[float]

    sparse_indices: list[int]

    sparse_values: list[float]

    payload: dict[str, Any] = Field(default_factory=dict)