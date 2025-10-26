from typing import Annotated

from src.modules.shared.dependencies.auth import DepCurrentUser

from fastapi import Depends
from src.modules.company.services.company import CompanyService
from src.modules.company.schemas.company import CompanyListResponseSchema


async def _list_companies(
    _current_user: DepCurrentUser,
    company_service: CompanyService,
    skip: int = 0,
    limit: int = 10,
):
    return await company_service.list_companies(skip, limit)


DepListCompanies = Annotated[
    CompanyListResponseSchema,
    Depends(_list_companies),
]
