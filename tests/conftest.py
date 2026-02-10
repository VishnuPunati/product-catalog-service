import os
import sys
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Ensure app is importable
sys.path.append(os.path.abspath("."))

from app.main import app
from app.database import Base


# --------------------
# Test Database
# --------------------

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://user:password@db:5432/product_catalog"
)



engine = create_engine(TEST_DATABASE_URL, future=True)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# --------------------
# Database Setup
# --------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# --------------------
# API Client
# --------------------

@pytest.fixture(scope="function")
def client():
    return TestClient(app)
