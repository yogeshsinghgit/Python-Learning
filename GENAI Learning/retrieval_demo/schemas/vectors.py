from pydantic import BaseModel


class DenseVector(BaseModel):
    values: list[float]


class SparseVectorData(BaseModel):
    indices: list[int]
    values: list[float]