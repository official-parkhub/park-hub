from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import SETTINGS

SQL_ASYNC_ENGINE = create_async_engine(
    SETTINGS.sqlalchemy_url,
    echo=SETTINGS.sqlalchemy_echo,
    future=True,
)

SQL_ENGINE = create_engine(
    SETTINGS.sqlalchemy_url,
    echo=SETTINGS.sqlalchemy_echo,
)

make_sql_session: sessionmaker[Session] = sessionmaker(
    expire_on_commit=False,
    bind=SQL_ENGINE,
)

make_sql_async_session: sessionmaker[AsyncSession] = sessionmaker(
    expire_on_commit=False,
    bind=SQL_ASYNC_ENGINE,
    class_=AsyncSession,
)
