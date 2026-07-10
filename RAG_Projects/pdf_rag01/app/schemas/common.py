from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """
    Base schema inherited by all application schemas.
    """

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }


class TimestampMixin(BaseModel):
    """
    Common timestamp fields.
    """

    created_at: datetime = Field(default_factory=datetime.utcnow)


class UUIDMixin(BaseModel):
    """
    Common UUID field.
    """

    id: UUID = Field(default_factory=uuid4)