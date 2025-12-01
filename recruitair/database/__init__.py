import os
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncContextManager, AsyncIterator, Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from .db_settings import DBSettings


def get_engine():
    settings = DBSettings()
    database_url = URL.create(
        drivername=settings.db_driver,
        username=settings.db_username,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_database,
    )
    engine = create_engine(database_url)
    return engine


def get_async_engine():
    settings = DBSettings()
    async_database_url = URL.create(
        drivername=settings.db_async_driver,
        username=settings.db_username,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_database,
    )
    async_engine = create_async_engine(async_database_url)
    return async_engine


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_engine = get_async_engine()
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)


def get_db_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


@asynccontextmanager
async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
