from fastapi import APIRouter

from src.modules.company.dependencies.company_price import (
    DepCreateParkingPrice,
    DepCreateParkingPriceException,
    DepListParkingPrices,
    DepParkingPriceReferences,
)

router = APIRouter(
    prefix="/company/{company_id}/price",
    tags=["Company Price"],
)


@router.post("/", status_code=201)
async def create_parking_price(
    response: DepCreateParkingPrice,
):
    """
    Create a new parking price.
    """
    return response


@router.post("/exception", status_code=201)
async def create_parking_price_exception(
    response: DepCreateParkingPriceException,
):
    """
    Create a new parking price exception.
    """
    return response


@router.get("/reference")
async def get_parking_price_references(
    result: DepParkingPriceReferences,
):
    """
    Get parking price references for a company.
    """
    return result


@router.get("/list")
async def list_parking_prices(
    result: DepListParkingPrices,
):
    """
    List all parking prices for a company.
    """
    return result
