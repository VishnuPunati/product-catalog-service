from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict



class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)

    description: Optional[str] = Field(
        None,
        max_length=2000
    )

    price: Decimal = Field(..., ge=0)

    sku: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Z0-9\-]+$"
    )



class ProductCreate(ProductBase):
    category_ids: Optional[List[UUID]] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)

    description: Optional[str] = Field(None, max_length=2000)

    price: Optional[Decimal] = Field(None, ge=0)

    sku: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Z0-9\-]+$"
    )

    category_ids: Optional[List[UUID]] = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    sku: str

    categories: List["CategoryResponse"]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


from app.schemas.category import CategoryResponse
