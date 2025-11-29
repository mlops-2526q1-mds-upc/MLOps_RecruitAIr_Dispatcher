import os
from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncIterator, Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

db_username = os.getenv("RECRUITAIR_DB_USERNAME", None)
db_password = os.getenv("RECRUITAIR_DB_PASSWORD", None)
db_host = os.getenv("RECRUITAIR_DB_HOST", None)
db_port = int(os.getenv("RECRUITAIR_DB_PORT", 5432))
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

async_database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=db_username,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_database,
)
async_engine = create_async_engine(async_database_url)
_make_async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


def get_session() -> Session:
    return _make_session()


@asynccontextmanager
async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with _make_async_session() as session:
        yield session
