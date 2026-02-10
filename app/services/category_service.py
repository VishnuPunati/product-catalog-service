from typing import List, Optional, Callable
from uuid import UUID

from app.models.category import Category
from app.unit_of_work.base import IUnitOfWork


class CategoryService:

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]):
        self.uow_factory = uow_factory

    def create_category(
        self,
        *,
        name: str,
        description: Optional[str] = None,
    ) -> Category:

        if not name.strip():
            raise ValueError("Category name must not be empty")

        with self.uow_factory() as uow:
            category = Category(
                name=name,
                description=description,
            )
            uow.categories.add(category)
            return category

    def get_category(self, category_id: UUID) -> Optional[Category]:
        with self.uow_factory() as uow:
            return uow.categories.get_by_id(category_id)

    def list_categories(self, skip: int = 0, limit: int = 10) -> List[Category]:
        with self.uow_factory() as uow:
            return uow.categories.get_all(skip, limit)

    def update_category(
        self,
        category_id: UUID,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Category]:

        if name is not None and not name.strip():
            raise ValueError("Category name must not be empty")

        with self.uow_factory() as uow:
            category = Category(
                name=name,
                description=description,
            )
            return uow.categories.update(category_id, category)

    def delete_category(self, category_id: UUID) -> bool:
        with self.uow_factory() as uow:
            return uow.categories.delete(category_id)
