from typing import Annotated

from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.shared.schemas.state import CreateStateSchema, StateWithIDSchema


from fastapi import Depends
from src.core import errors
from src.modules.shared.services.geo import GeoService


async def _create_state(
    state: CreateStateSchema,
    geo_service: GeoService,
    user: DepCurrentUser,
) -> StateWithIDSchema:
    if not user.is_admin:
        raise errors.AuthorizationError(
            message="Insufficient permissions to create state"
        )

    return await geo_service.create_state(state)


DepCreateState = Annotated[
    StateWithIDSchema,
    Depends(_create_state),
]
