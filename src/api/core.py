from api.routers.health import router as health_router
from src.modules.driver.routers.customer import router as customer_router
from src.modules.shared.routers.login import router as login_router
from src.modules.company.routers import router as organization_router
from src.modules.company.routers.company import (
    router as company_router,
    image_router as company_image_router,
)
from src.modules.shared.routers.geo import router as geo_router

from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from src.api.shared import add_exception_handlers, add_middlewares
from src.settings import SETTINGS


def add_routers(base_router: FastAPI | APIRouter):
    routers = [
        health_router,
        customer_router,
        login_router,
        organization_router,
        company_router,
        company_image_router,
        geo_router,
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
