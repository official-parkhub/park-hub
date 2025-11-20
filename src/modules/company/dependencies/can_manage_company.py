from typing import Annotated
import uuid
from src.modules.company.services.company import CompanyService
from src.modules.shared.dependencies.auth import DepCurrentUser
from fastapi import Depends


async def _can_manage_company(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: uuid.UUID,
) -> bool:
    existing_company = await company_service.get_company_by_id(str(company_id))
    return current_user.is_admin or (
        existing_company.organization_id is not None
        and current_user.organization is not None
        and existing_company.organization_id == current_user.organization.id
    )


DepCanManageCompany = Annotated[
    bool,
    Depends(_can_manage_company),
]
