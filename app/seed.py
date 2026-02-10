from app.database import SessionLocal
from app.models.product import Product
from app.models.category import Category

def seed():
    session = SessionLocal()

    electronics = Category(name="Electronics")
    fashion = Category(name="Fashion")
    books = Category(name="Books")

    session.add_all([electronics, fashion, books])
    session.flush()

    products = [
        Product(name="Phone", price=15000, sku="SKU1", categories=[electronics]),
        Product(name="Laptop", price=55000, sku="SKU2", categories=[electronics]),
        Product(name="T-Shirt", price=500, sku="SKU3", categories=[fashion]),
        Product(name="Novel", price=300, sku="SKU4", categories=[books]),
    ]

    session.add_all(products)
    session.commit()
    session.close()

if __name__ == "__main__":
    seed()
