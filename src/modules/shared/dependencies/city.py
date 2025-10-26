from typing import Annotated

from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.shared.schemas.city import CreateCitySchema, CityWithIDSchema

from fastapi import Depends
from src.core import errors
from src.modules.shared.services.geo import GeoService


async def _create_city(
    city: CreateCitySchema,
    geo_service: GeoService,
    user: DepCurrentUser,
) -> CityWithIDSchema:
    if not user.is_admin:
        raise errors.AuthorizationError(
            message="Insufficient permissions to create city"
        )
    return await geo_service.create_city(city)


DepCreateCity = Annotated[
    CityWithIDSchema,
    Depends(_create_city),
]
