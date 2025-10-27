from fastapi import APIRouter

from src.modules.company.schemas.organization import (
    OrganizationCreateSchema,
    OrganizationResponseSchema,
)
from src.modules.company.services.organization import OrganizationService
from src.modules.shared.schemas.user import UserCreateSchema
from src.modules.shared.services.user import UserService

router = APIRouter(tags=["Organization"])


@router.post("/organization", status_code=201)
async def create_organization(
    organization: OrganizationCreateSchema,
    user: UserCreateSchema,
    user_service: UserService,
    organization_service: OrganizationService,
) -> OrganizationResponseSchema:
    """
    Create a new organization.
    """
    user = await user_service.create_user(user)
    result = await organization_service.create_organization(user.id, organization)
    return result
