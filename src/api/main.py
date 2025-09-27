from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.core import create_core_app
# from app.modules import models
from src.settings import SETTINGS

# Ensure models are imported to register them with SQLAlchemy
# 'assert models' is used to avoid unused import warnings
# assert models


@asynccontextmanager
async def lifespan(app: FastAPI):
    core_docs_url = "disabled"
    if SETTINGS.feat_enable_core_docs:
        core_docs_url = f"http://127.0.0.1:{SETTINGS.api_port}/api/core/docs"

    print(f"Core API documentation: {core_docs_url}")
    yield


def create_app():
    app = FastAPI(
        title="ParkHub API",
        version=SETTINGS.api_version,
        docs_url=None,
        openapi_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    core_app = create_core_app()

    app.mount("/api/core", core_app)
    return app


app = create_app()
