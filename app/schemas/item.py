from datetime import datetime

from pydantic import BaseModel, Field


# Schema for creating an item
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    description: str | None = Field(None, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    is_active: bool = Field(True, description="Whether the item is active")


# Schema for updating an item (all fields optional)
class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: float | None = Field(None, gt=0)
    is_active: bool | None = None


# Schema for item responses
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
