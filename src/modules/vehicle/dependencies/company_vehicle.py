from typing import Annotated

from fastapi import Depends
from src.core import errors
from src.modules.company.services.company import CompanyService
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.vehicle.schemas.vehicle import (
    UpsertVehicleSchema,
    VehicleEntranceInputSchema,
    VehicleEntranceResponseSchema,
)
from src.modules.vehicle.services.company_vehicle import CompanyVehicleService
from src.modules.vehicle.services.customer_vehicle import CustomerVehicleService


async def _register_vehicle_entrance(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: str,
    input_data: VehicleEntranceInputSchema,
    customer_vehicle_service: CustomerVehicleService,
    company_vehicle_service: CompanyVehicleService,
    company_price_service: CompanyPriceService,
) -> VehicleEntranceResponseSchema:
    existing_company = await company_service.get_company_by_id(company_id)
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to create parking price exceptions for this company"
        )

    vehicle = await customer_vehicle_service.upsert_vehicle(
        vehicle_data=UpsertVehicleSchema(
            plate=input_data.plate,
        )
    )

    existing_vehicle_entrance = (
        await company_vehicle_service.get_active_vehicle_entrance(
            vehicle_id=str(vehicle.id),
            company_id=company_id,
        )
    )

    if existing_vehicle_entrance:
        raise errors.InvalidOperation(message="Vehicle already has an active entrance")

    vehicle_entrance = await company_vehicle_service.register_vehicle_entrance(
        company_price_service=company_price_service,
        company_id=company_id,
        vehicle_id=str(vehicle.id),
    )

    return vehicle_entrance


DepRegisterVehicleEntrance = Annotated[
    VehicleEntranceResponseSchema,
    Depends(_register_vehicle_entrance),
]
