from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base import IRepository


class CategoryRepository(IRepository[Category]):

    def __init__(self, session: Session):
        self.session = session

    def add(self, category: Category) -> Category:
        self.session.add(category)
        return category

    def get_by_id(self, id: UUID) -> Optional[Category]:
        return (
            self.session
            .query(Category)
            .filter(Category.id == id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Category]:
        return (
            self.session
            .query(Category)
            .order_by(Category.name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, id: UUID, category: Category) -> Optional[Category]:
        db_category = self.get_by_id(id)

        if not db_category:
            return None

        if category.name is not None:
            db_category.name = category.name

        if category.description is not None:
            db_category.description = category.description

        return db_category

    def delete(self, id: UUID) -> bool:
        category = self.get_by_id(id)

        if not category:
            return False

        self.session.delete(category)
        return True
