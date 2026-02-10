from abc import ABC, abstractmethod

from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository


class IUnitOfWork(ABC):
    """
    Unit of Work interface.

    Responsibilities:
    - Manage transaction boundaries
    - Expose repositories
    - Commit or rollback atomically
    """

    products: ProductRepository
    categories: CategoryRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.dispose()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def dispose(self):
        pass
