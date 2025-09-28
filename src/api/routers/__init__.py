from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["Ping"])
def health_check():
    return {"status": "ok"}
