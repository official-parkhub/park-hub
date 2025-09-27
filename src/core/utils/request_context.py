from typing import Annotated

from fastapi import BackgroundTasks, Depends, Request, Response
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.session import make_sql_async_session
from src.core.utils.depends import dependable
from src.core import errors


async def get_async_session():
    db = make_sql_async_session()
    try:
        yield db
    except Exception as e:
        if not isinstance(e, errors.ApplicationError) or e.should_rollback:
            logger.exception("Exception was caught. Rolling back transaction.")
            await db.rollback()
        raise
    else:
        await db.commit()
    finally:
        await db.close()


@dependable
class RequestContext:
    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_async_session)],
        bg: BackgroundTasks,
        request: Request,
        response: Response,
    ):
        self.db = db
        self.bg = bg
        self.request = request
        self.response = response

class RequestContextUser:
    def __init__(self, rc: RequestContext):
        self.rc = rc

    @property
    def db(self):
        return self.rc.db

    @property
    def bg(self):
        return self.rc.bg

    @property
    def request(self):
        return self.rc.request

    @property
    def response(self):
        return self.rc.response
