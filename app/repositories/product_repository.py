from typing import List, Optional
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base import IRepository


class ProductRepository(IRepository[Product]):

    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product) -> Product:
        self.session.add(product)
        return product

    def get_by_id(self, id: UUID) -> Optional[Product]:
        return (
            self.session
            .query(Product)
            .filter(Product.id == id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Product]:
        return (
            self.session
            .query(Product)
            .order_by(Product.name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, id: UUID, product: Product) -> Optional[Product]:
        db_product = self.get_by_id(id)

        if not db_product:
            return None

        if product.name is not None:
            db_product.name = product.name

        if product.description is not None:
            db_product.description = product.description

        if product.price is not None:
            db_product.price = product.price

        if product.sku is not None:
            db_product.sku = product.sku

        return db_product

    def delete(self, id: UUID) -> bool:
        product = self.get_by_id(id)

        if not product:
            return False

        self.session.delete(product)
        return True

    # Advanced Search (FULL-TEXT SEARCH)
    def search(
        self,
        keyword: Optional[str] = None,
        category_id: Optional[UUID] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Product]:

        query = self.session.query(Product)

        if keyword:
            query = query.filter(
                text(
                    "to_tsvector('english', products.name || ' ' || "
                    "COALESCE(products.description, '')) "
                    "@@ plainto_tsquery('english', :keyword)"
                )
            ).params(keyword=keyword)

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if category_id:
            query = (
                query
                .join(Product.categories)
                .filter_by(id=category_id)
                .distinct()
            )

        return (
            query
            .order_by(Product.name)
            .offset(skip)
            .limit(limit)
            .all()
        )
