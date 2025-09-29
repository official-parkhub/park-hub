from sqlalchemy import select

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.company.models.organization import Organization
from src.modules.company.schemas.organization import OrganizationCreateSchema
from src.modules.shared.models.geo.state import State


@dependable
class OrganizationService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def get_organization_by_id(self, id: str):
        result = await self.db.execute(
            select(Organization).where(Organization.id == id)
        )
        organization = result.scalars().first()
        if not organization:
            raise errors.ResourceNotFound(message="Organization not found")
        return organization

    async def create_organization(
        self,
        user_id: str,
        organization: OrganizationCreateSchema,
    ) -> Organization:
        state = await self.db.execute(
            select(State).where(State.id == organization.state_id)
        )

        if not state.scalars().first():
            raise errors.ResourceNotFound(message="State not found")

        db_organization = Organization(
            user_id=user_id,
            name=organization.name,
            register_code=organization.register_code,
            state_id=organization.state_id,
        )
        self.db.add(db_organization)
        await self.db.flush()
        await self.db.refresh(db_organization)

        return await self.get_organization_by_id(db_organization.id)
