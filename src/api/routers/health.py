from fastapi import APIRouter, HTTPException

from src.core.database.ready import is_db_running

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    postgres_health = is_db_running()
    detail = {
        "postgres": postgres_health,
    }

    if not postgres_health:
        raise HTTPException(
            status_code=503,
            detail=detail,
        )
    return {
        "status": "ok",
        "detail": detail,
    }
