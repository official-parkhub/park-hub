from typing import Annotated, TypeAlias
import uuid

from fastapi import Depends
from src.core import errors
from src.modules.company.services.company import CompanyService
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.vehicle.schemas.vehicle import (
    ListActiveVehiclesResponseSchema,
    UpsertVehicleSchema,
    VehicleEntranceInputSchema,
    VehicleEntranceResponseSchema,
    VehicleExitInputSchema,
    VehicleExitResponseSchema,
)
from src.modules.vehicle.services.company_vehicle import CompanyVehicleService
from src.modules.vehicle.services.customer_vehicle import CustomerVehicleService


async def _register_vehicle_entrance(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: uuid.UUID,
    input_data: VehicleEntranceInputSchema,
    customer_vehicle_service: CustomerVehicleService,
    company_vehicle_service: CompanyVehicleService,
    company_price_service: CompanyPriceService,
) -> VehicleEntranceResponseSchema:
    existing_company = await company_service.get_company_by_id(str(company_id))
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
            company_id=str(company_id),
        )
    )

    if existing_vehicle_entrance:
        raise errors.InvalidOperation(message="Vehicle already has an active entrance")

    vehicle_entrance = await company_vehicle_service.register_vehicle_entrance(
        company_price_service=company_price_service,
        company_id=str(company_id),
        vehicle_id=str(vehicle.id),
    )

    return vehicle_entrance


async def _register_vehicle_exit(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_vehicle_service: CompanyVehicleService,
    customer_vehicle_service: CustomerVehicleService,
    vehicle_exit_input: VehicleExitInputSchema,
    company_id: uuid.UUID,
) -> VehicleExitResponseSchema:
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to register vehicle exits for this company"
        )

    vehicle = await customer_vehicle_service.get_vehicle_by_plate(
        plate=vehicle_exit_input.plate,
    )

    if not vehicle:
        raise errors.ResourceNotFound(message="Vehicle not found")

    vehicle_entrance = await company_vehicle_service.get_active_vehicle_entrance(
        vehicle_id=str(vehicle.id),
        company_id=str(company_id),
    )

    if not vehicle_entrance:
        raise errors.InvalidOperation(
            message="Vehicle does not have an active entrance"
        )

    vehicle_exit = await company_vehicle_service.register_vehicle_exit(
        vehicle_entrance_id=str(vehicle_entrance.id),
        ended_at=vehicle_exit_input.ended_at,
    )

    return vehicle_exit


async def _list_active_vehicles(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_vehicle_service: CompanyVehicleService,
    company_id: uuid.UUID,
    skip: int = 0,
    limit: int = 10,
) -> ListActiveVehiclesResponseSchema:
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to list active vehicles for this company"
        )

    active_vehicles = await company_vehicle_service.list_active_vehicles_by_company(
        company_id=str(company_id),
        skip=skip,
        limit=limit,
    )

    return active_vehicles


async def _list_vehicles(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_vehicle_service: CompanyVehicleService,
    company_id: uuid.UUID,
    skip: int = 0,
    limit: int = 10,
) -> ListActiveVehiclesResponseSchema:
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to list active vehicles for this company"
        )

    active_vehicles = await company_vehicle_service.list_vehicles_by_company(
        company_id=str(company_id),
        skip=skip,
        limit=limit,
    )

    return active_vehicles


DepRegisterVehicleEntrance: TypeAlias = Annotated[
    VehicleEntranceResponseSchema,
    Depends(_register_vehicle_entrance),
]

DepRegisterVehicleExit: TypeAlias = Annotated[
    VehicleExitResponseSchema,
    Depends(_register_vehicle_exit),
]

DepListCompanyActiveVehicles: TypeAlias = Annotated[
    ListActiveVehiclesResponseSchema,
    Depends(_list_active_vehicles),
]

DepListCompanyVehicles: TypeAlias = Annotated[
    ListActiveVehiclesResponseSchema,
    Depends(_list_vehicles),
]
