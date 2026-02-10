from typing import List, Optional, Callable
from decimal import Decimal
from uuid import UUID

from app.models.product import Product
from app.models.category import Category
from app.unit_of_work.base import IUnitOfWork


class ProductService:

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]):
        self.uow_factory = uow_factory

    def create_product(
        self,
        *,
        name: str,
        price: Decimal,
        sku: str,
        description: Optional[str] = None,
        category_ids: Optional[List[UUID]] = None,
    ) -> Product:

        if price < 0:
            raise ValueError("Price must be non-negative")

        with self.uow_factory() as uow:
            product = Product(
                name=name,
                price=price,
                sku=sku,
                description=description,
            )

            if category_ids:
                categories = [
                    uow.categories.get_by_id(category_id)
                    for category_id in category_ids
                ]

                if any(category is None for category in categories):
                    raise ValueError("One or more categories not found")

                product.categories = categories  # type: ignore

            uow.products.add(product)
            return product

    def get_product(self, product_id: UUID) -> Optional[Product]:
        with self.uow_factory() as uow:
            return uow.products.get_by_id(product_id)

    def list_products(self, skip: int = 0, limit: int = 10) -> List[Product]:
        with self.uow_factory() as uow:
            return uow.products.get_all(skip, limit)

    def update_product(
        self,
        product_id: UUID,
        *,
        name: Optional[str] = None,
        price: Optional[Decimal] = None,
        sku: Optional[str] = None,
        description: Optional[str] = None,
        category_ids: Optional[List[UUID]] = None,
    ) -> Optional[Product]:

        if price is not None and price < 0:
            raise ValueError("Price must be non-negative")

        with self.uow_factory() as uow:
            product = Product(
                name=name,
                price=price,
                sku=sku,
                description=description,
            )

            updated = uow.products.update(product_id, product)

            if not updated:
                return None

            if category_ids is not None:
                categories = [
                    uow.categories.get_by_id(category_id)
                    for category_id in category_ids
                ]

                if any(category is None for category in categories):
                    raise ValueError("One or more categories not found")

                updated.categories = categories  # type: ignore

            return updated

    def delete_product(self, product_id: UUID) -> bool:
        with self.uow_factory() as uow:
            return uow.products.delete(product_id)

    def search_products(
        self,
        *,
        keyword: Optional[str] = None,
        category_id: Optional[UUID] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Product]:

        if min_price is not None and min_price < 0:
            raise ValueError("min_price must be non-negative")

        if max_price is not None and max_price < 0:
            raise ValueError("max_price must be non-negative")

        with self.uow_factory() as uow:
            return uow.products.search(
                keyword=keyword,
                category_id=category_id,
                min_price=min_price,
                max_price=max_price,
                skip=skip,
                limit=limit,
            )
