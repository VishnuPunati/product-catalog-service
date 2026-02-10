import uuid

from sqlalchemy import Column, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.product_category import product_categories


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(Text, nullable=False)

    description = Column(Text)

    price = Column(DECIMAL(10, 2), nullable=False)

    sku = Column(Text, unique=True, nullable=False)

    categories = relationship(
        "Category",
        secondary=product_categories,
        back_populates="products",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name} sku={self.sku}>"
