from fastapi import APIRouter

from src.modules.company.dependencies.company_price import DepCreateParkingPrice

router = APIRouter(
    prefix="/company/{company_id}/price",
    tags=["Company Price"],
)


@router.post("/")
async def create_parking_price(
    response: DepCreateParkingPrice,
):
    """
    Create a new parking price.
    """
    return response
