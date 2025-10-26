from typing import Annotated

from src.modules.company.schemas.company.company import CompleteCompanySchema
from src.modules.company.schemas.company.create_company import CreateCompanySchema
from src.modules.shared.dependencies.auth import DepCurrentUser

from fastapi import Depends
from src.modules.company.services.company import CompanyService

from src.core import errors


async def _create_company(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    create_company_schema: CreateCompanySchema,
):
    if not current_user.organization:
        raise errors.ResourceNotFound(message="User has no organization")

    return await company_service.create_company(
        organization_id=current_user.organization.id,
        create_company_schema=create_company_schema,
    )


DepCreateCompany = Annotated[
    CompleteCompanySchema,
    Depends(_create_company),
]
