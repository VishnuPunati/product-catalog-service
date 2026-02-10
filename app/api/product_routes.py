from typing import List, Optional
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query, Response

from app.services.product_service import ProductService
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.unit_of_work.sqlalchemy_uow import SQLAlchemyUnitOfWork


router = APIRouter(prefix="/products", tags=["Products"])


# Dependency
def get_product_service() -> ProductService:
    return ProductService(SQLAlchemyUnitOfWork)


# --------------------
# Search
# --------------------

@router.get(
    "/search",
    response_model=List[ProductResponse]
)
def search_products(
    q: Optional[str] = Query(None, min_length=1),
    category_id: Optional[UUID] = None,
    min_price: Optional[Decimal] = Query(None, ge=0),
    max_price: Optional[Decimal] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.search_products(
            keyword=q,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------
# Create
# --------------------

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse
)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.create_product(
            name=payload.name,
            price=payload.price,
            sku=payload.sku,
            description=payload.description,
            category_ids=payload.category_ids,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------
# List
# --------------------

@router.get(
    "",
    response_model=List[ProductResponse]
)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    return service.list_products(skip, limit)


# --------------------
# Get By ID
# --------------------

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    product = service.get_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# --------------------
# Update
# --------------------

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    try:
        product = service.update_product(
            product_id,
            name=payload.name,
            price=payload.price,
            sku=payload.sku,
            description=payload.description,
            category_ids=payload.category_ids,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# --------------------
# Delete
# --------------------

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    deleted = service.delete_product(product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
