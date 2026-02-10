from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID


T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """
    Base repository interface.

    NOTE:
    - Repositories must NOT commit transactions.
    - Transaction control is handled by Unit of Work.
    """

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, id: UUID, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass
