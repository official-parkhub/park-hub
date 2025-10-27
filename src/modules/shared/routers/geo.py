from fastapi import APIRouter

from src.modules.shared.dependencies.state import DepCreateState
from src.modules.shared.dependencies.city import DepCreateCity
from src.modules.shared.schemas.state import StateWithIDSchema
from src.modules.shared.schemas.city import CityWithIDSchema

router = APIRouter(
    tags=["Geo"],
    prefix="/geo",
)


@router.post("/state", status_code=201)
async def create_state(
    response: DepCreateState,
) -> StateWithIDSchema:
    return response


@router.post("/city", status_code=201)
async def create_city(
    response: DepCreateCity,
) -> CityWithIDSchema:
    return response
