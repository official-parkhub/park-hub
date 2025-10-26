from typing_extensions import Annotated
from fastapi import Depends
from src.core import errors
from src.modules.company.schemas.company.company_price import (
    CreateParkingPriceResponseSchema,
    CreateParkingPriceSchema,
)
from src.modules.company.services.company import CompanyService
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.shared.dependencies.auth import DepCurrentUser


async def _create_parking_price(
    current_user: DepCurrentUser,
    company_price_service: CompanyPriceService,
    parking_price_schema: CreateParkingPriceSchema,
    company_service: CompanyService,
) -> CreateParkingPriceResponseSchema:
    existing_company = await company_service.get_company_by_id(
        parking_price_schema.company_id
    )
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to create parking prices for this company"
        )

    return await company_price_service.create_parking_price(parking_price_schema)


DepCreateParkingPrice = Annotated[
    CreateParkingPriceResponseSchema,
    Depends(_create_parking_price),
]
