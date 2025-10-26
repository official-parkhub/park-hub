import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.core import errors
from src.settings import SETTINGS


def add_middlewares(app: FastAPI):
    if SETTINGS.feat_allow_wildcard_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(errors.ApplicationError)
    async def _(request: Request, exc: errors.ApplicationError):
        return exc.to_fastapi_response()

    @app.exception_handler(Exception)
    async def _(request: Request, exc: Exception):
        generic_error = errors.InternalServerError()
        return generic_error.to_fastapi_response()
