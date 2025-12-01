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

from recruitair.api import app
from recruitair.database import engine, get_db_session
from recruitair.database.models import Base


def override_get_db_session() -> Iterator:
    session_generator = get_db_session()
    session = next(session_generator)
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
