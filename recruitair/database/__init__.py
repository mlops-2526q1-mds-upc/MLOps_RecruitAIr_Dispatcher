import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

db_username = os.getenv("RECRUITAIR_DB_USERNAME", None)
db_password = os.getenv("RECRUITAIR_DB_PASSWORD", None)
db_host = os.getenv("RECRUITAIR_DB_HOST", None)
db_port = os.getenv("RECRUITAIR_DB_PORT", "5432")
db_database = os.getenv("RECRUITAIR_DB_DATABASE", None)

if not all([db_username, db_password, db_host, db_database]):
    raise ValueError("Database configuration environment variables are not fully set.")

database_url = URL.create(
    drivername="postgresql",
    username=db_username,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_database,
    # postgresql://user:password@host:port/database
)
engine = create_engine(database_url)
_make_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    return _make_session()
