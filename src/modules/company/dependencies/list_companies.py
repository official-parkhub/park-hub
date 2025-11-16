from typing import Annotated

from fastapi.params import Query

from src.core import errors
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.shared.dependencies.auth import DepCurrentUser

from fastapi import Depends
from src.modules.company.services.company import CompanyService
from src.modules.company.schemas.company.company_price import CompanyListResponseSchema


async def _list_companies(
    _current_user: DepCurrentUser,
    company_service: CompanyService,
    company_price_service: CompanyPriceService,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=10),
    only_owned: bool = Query(False),
):
    if only_owned:
        organization_id = (
            _current_user.organization.id if _current_user.organization else None
        )

        if not organization_id:
            raise errors.InvalidOperation(
                message="User does not belong to any organization"
            )

    return await company_service.list_companies(
        skip=skip,
        limit=limit,
        company_price_service=company_price_service,
        organization_id=organization_id if only_owned else None,
    )


DepListCompanies = Annotated[
    CompanyListResponseSchema,
    Depends(_list_companies),
]
