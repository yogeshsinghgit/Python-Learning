from pydantic import BaseModel, Field


class AttractionQuery(BaseModel):
    """Input to any AttractionProvider. Deliberately vendor-agnostic."""

    location: str = Field(
        description="City or destination to find attractions in, e.g. 'Goa'."
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=30,
        description="Maximum number of attractions to return.",
    )


class Attraction(BaseModel):
    name: str
    category: str
    distance_meters: float | None = None


class AttractionResult(BaseModel):
    location: str
    attractions: list[Attraction]
