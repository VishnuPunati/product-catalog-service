import uuid

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.product_category import product_categories


class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(Text, unique=True, nullable=False)

    description = Column(Text)

    products = relationship(
        "Product",
        secondary=product_categories,
        back_populates="categories",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name}>"
