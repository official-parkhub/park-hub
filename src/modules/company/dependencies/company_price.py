from typing_extensions import Annotated
from typing import TypeAlias
import uuid
from fastapi import Depends
from src.core import errors
from src.modules.company.schemas.company.company_price import (
    CreateParkingPriceExceptionResponseSchema,
    CreateParkingPriceExceptionSchema,
    CreateParkingPriceResponseSchema,
    CreateParkingPriceSchema,
    ListParkingPricesResponseSchema,
    ParkingPriceReferenceSchema,
)
from src.modules.company.services.company import CompanyService
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.shared.dependencies.auth import DepCurrentUser


async def _create_parking_price(
    current_user: DepCurrentUser,
    company_price_service: CompanyPriceService,
    parking_price_schema: CreateParkingPriceSchema,
    company_service: CompanyService,
    company_id: uuid.UUID,
) -> CreateParkingPriceResponseSchema:
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to create parking prices for this company"
        )

    return await company_price_service.create_parking_price(
        company_id=str(company_id),
        parking_price_schema=parking_price_schema,
    )


async def _create_parking_price_exception(
    current_user: DepCurrentUser,
    company_price_service: CompanyPriceService,
    create_parking_price_exception_schema: CreateParkingPriceExceptionSchema,
    company_service: CompanyService,
    company_id: uuid.UUID,
) -> CreateParkingPriceExceptionResponseSchema:
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to create parking price exceptions for this company"
        )

    return await company_price_service.create_parking_price_exception(
        company_id=str(company_id),
        create_parking_price_exception_schema=create_parking_price_exception_schema,
    )


async def _get_parking_price_references(
    _current_user: DepCurrentUser,
    company_price_service: CompanyPriceService,
    company_id: uuid.UUID,
) -> ParkingPriceReferenceSchema:
    price_reference = await company_price_service.get_parking_price_reference(
        str(company_id)
    )

    if not price_reference:
        raise errors.ResourceNotFound(
            message="No parking price reference found for the given company"
        )
    return price_reference


async def _list_parking_prices(
    _current_user: DepCurrentUser,
    company_price_service: CompanyPriceService,
    company_id: uuid.UUID,
) -> ListParkingPricesResponseSchema:
    parking_prices = await company_price_service.list_parking_prices(str(company_id))

    return parking_prices


DepParkingPriceReferences: TypeAlias = Annotated[
    ParkingPriceReferenceSchema,
    Depends(_get_parking_price_references),
]

DepCreateParkingPrice: TypeAlias = Annotated[
    CreateParkingPriceResponseSchema,
    Depends(_create_parking_price),
]

DepCreateParkingPriceException: TypeAlias = Annotated[
    CreateParkingPriceExceptionResponseSchema,
    Depends(_create_parking_price_exception),
]

DepListParkingPrices: TypeAlias = Annotated[
    ListParkingPricesResponseSchema,
    Depends(_list_parking_prices),
]
