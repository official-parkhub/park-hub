import subprocess

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.core.database.session import make_sql_session
from loguru import logger


def is_db_running() -> bool:
    try:
        with make_sql_session() as session:
            session.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database is not running: {e}")
        return False


def is_db_up_to_date() -> bool:
    try:
        result = subprocess.run(["alembic", "check"], text=True, capture_output=True)
        return "database is not up to date" not in result.stdout
    except SQLAlchemyError:
        return False
