from pydantic import BaseModel, ConfigDict, Field


class QueryVector(BaseModel):
    """
    Represents the vectorized form of a query.

    This model is provider-independent and is consumed by
    the retrieval pipeline.
    """

    model_config = ConfigDict(frozen=True)

    dense_vector: list[float] = Field(
        description="Dense embedding of the query."
    )

    sparse_indices: list[int] = Field(
        default_factory=list,
        description="Sparse vector indices."
    )

    sparse_values: list[float] = Field(
        default_factory=list,
        description="Sparse vector values."
    )