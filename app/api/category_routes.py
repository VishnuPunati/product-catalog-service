from typing import List
from uuid import UUID

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    Query,
    Response,
)

from app.services.category_service import CategoryService
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)
from app.unit_of_work.sqlalchemy_uow import SQLAlchemyUnitOfWork


router = APIRouter(prefix="/categories", tags=["Categories"])


# Dependency
def get_category_service() -> CategoryService:
    return CategoryService(SQLAlchemyUnitOfWork)


# --------------------
# Create
# --------------------

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse
)
def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    try:
        return service.create_category(
            name=payload.name,
            description=payload.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------
# Get By ID
# --------------------

@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_category(category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


# --------------------
# List
# --------------------

@router.get(
    "",
    response_model=List[CategoryResponse]
)
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return service.list_categories(skip, limit)


# --------------------
# Update
# --------------------

@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    try:
        category = service.update_category(
            category_id,
            name=payload.name,
            description=payload.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


# --------------------
# Delete
# --------------------

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
):
    deleted = service.delete_category(category_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
