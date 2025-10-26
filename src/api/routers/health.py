from fastapi import APIRouter, HTTPException

from src.core.database.ready import is_db_running, is_db_up_to_date

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    postgres_running = is_db_running()
    postgres_up_to_date = is_db_up_to_date()
    postgres_health = postgres_running and postgres_up_to_date
    detail = {
        "postgres": {
            "running": postgres_running,
            "up_to_date": postgres_up_to_date,
        },
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
