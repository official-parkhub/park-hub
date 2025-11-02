import os
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tests.helpers.db_utils import (
    build_db_url_from_env,
    clear_database_using_url,
    run_migrations,
    wait_for_db,
)

from fastapi.testclient import TestClient


DB_WAIT_TIMEOUT = float(os.getenv("TEST_DB_WAIT_TIMEOUT", "30"))


@pytest.fixture(scope="session", autouse=True)
def _prepare_db() -> None:
    url = build_db_url_from_env()
    wait_for_db(url, timeout=DB_WAIT_TIMEOUT)
    run_migrations()
    clear_database_using_url(url)


@pytest.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    url = build_db_url_from_env()
    echo = os.getenv("SQLALCHEMY_ECHO", "false").lower() in {"1", "true", "yes", "on"}
    engine = create_async_engine(url, echo=echo, future=True)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="session")
def async_session_maker(async_engine: AsyncEngine):
    return sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
async def db(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def app():
    from src.api.main import app

    return app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def rc(db):
    class _RC:
        def __init__(self, db_session):
            self.db = db_session

    return _RC(db)
