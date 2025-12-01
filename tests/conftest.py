import os
import sys
from typing import Iterator

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
from fastapi.testclient import TestClient

os.environ["RECRUITAIR_DB_DRIVER"] = "sqlite"
os.environ["RECRUITAIR_DB_ASYNC_DRIVER"] = "sqlite+aiosqlite"
os.environ["RECRUITAIR_DB_DATABASE"] = ":memory:"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from recruitair.api import app
from recruitair.database import get_db_session
from recruitair.database.models import Base

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_database():
    # Drop all the tables before each test, and create them anew
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all the tables after each test
    Base.metadata.drop_all(bind=engine)


def override_get_db_session() -> Iterator:
    session = TestSessionLocal()
    # Create all the tables (it is an in-memory DB)
    Base.metadata.create_all(bind=engine)
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db_session] = override_get_db_session


# --------- FASTAPI TEST CLIENT ---------
@pytest.fixture
def client():
    return TestClient(app)
