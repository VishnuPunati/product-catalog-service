import os

APP_NAME = os.getenv("APP_NAME", "Product Catalog Service")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@localhost:5432/product_catalog"
)
