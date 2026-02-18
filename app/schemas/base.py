from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# Standard paginated response wrapper
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int


# Reusable pagination query parameters
class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Max records to return")
