from typing import Optional

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.unit_of_work.base import IUnitOfWork


class SQLAlchemyUnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session: Optional[Session] = None
        self._products: Optional[ProductRepository] = None
        self._categories: Optional[CategoryRepository] = None

    # -----------------
    # Context Manager
    # -----------------

    def __enter__(self):
        if self.session is not None:
            raise RuntimeError("UnitOfWork already started")

        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

        self.dispose()

    # -----------------
    # Repositories
    # -----------------

    @property
    def products(self) -> ProductRepository:
        if not self._products:
            raise RuntimeError("UnitOfWork not started")
        return self._products

    @property
    def categories(self) -> CategoryRepository:
        if not self._categories:
            raise RuntimeError("UnitOfWork not started")
        return self._categories

    # -----------------
    # Transaction Control
    # -----------------

    def _start(self):
        self.session = SessionLocal()
        self._products = ProductRepository(self.session)
        self._categories = CategoryRepository(self.session)

    def commit(self):
        if self.session:
            self.session.commit()

    def rollback(self):
        if self.session:
            self.session.rollback()

    def dispose(self):
        if self.session:
            self.session.close()

        self.session = None
        self._products = None
        self._categories = None
