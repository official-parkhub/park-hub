from api.routers.health import router as health_router
from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from src.api.shared import add_exception_handlers, add_middlewares
from src.settings import SETTINGS


def add_routers(base_router: FastAPI | APIRouter):
    routers = [
        health_router,
    ]
    for r in routers:
        base_router.include_router(r)


def create_core_app():
    app = FastAPI(
        title="ParkHub Core API",
        version=SETTINGS.api_version,
        docs_url="/docs" if SETTINGS.feat_enable_core_docs else None,
        openapi_url="/openapi.json" if SETTINGS.feat_enable_core_docs else None,
        redoc_url=None,
    )

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/api/core/docs")

    add_routers(app)
    add_exception_handlers(app)
    add_middlewares(app)
    return app


app = create_core_app()
