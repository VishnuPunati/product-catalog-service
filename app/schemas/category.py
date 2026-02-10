from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

    description: Optional[str] = Field(
        None,
        max_length=1000
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)

    description: Optional[str] = Field(None, max_length=1000)



class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
