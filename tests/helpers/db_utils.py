import os
import time
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from alembic import command
from alembic.config import Config


def find_repo_root(start: Path | None = None) -> Path:
    """Ascend directories until 'alembic.ini' is found, return that folder."""
    cur = (start or Path(__file__).resolve()).parent
    for _ in range(8):
        if (cur / "alembic.ini").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return cur


def build_db_url_from_env() -> str:
    user = quote_plus(os.environ["POSTGRES_USER"])
    password = quote_plus(os.environ["POSTGRES_PASSWORD"])
    database = os.environ["POSTGRES_DATABASE"]
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


def wait_for_db(url: str, timeout: float = 30.0) -> None:
    start = time.time()
    last_err: Exception | None = None
    while time.time() - start < timeout:
        try:
            engine = create_engine(url, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            engine.dispose()
            return
        except Exception as e:
            last_err = e
            time.sleep(1)
    if last_err:
        raise last_err


def run_migrations(repo_root: Path | None = None) -> None:
    repo = find_repo_root(repo_root)
    cfg = Config(str(repo / "alembic.ini"))
    command.upgrade(cfg, "head")
