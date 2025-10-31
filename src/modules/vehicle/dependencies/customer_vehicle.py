from typing import Annotated, TypeAlias
import uuid

from fastapi import Depends, Query
from src.core import errors
from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.vehicle.schemas.vehicle import (
    CreateVehicleOwnerResponseSchema,
    CreateVehicleOwnerSchema,
    ListActiveVehiclesResponseSchema,
    ListVehicleByCustomerResponseSchema,
    VehicleStatisticsResponseSchema,
)
from src.modules.vehicle.services.customer_vehicle import CustomerVehicleService


async def _upsert_customer_vehicle(
    User: DepCurrentUser,
    vehicle_data: CreateVehicleOwnerSchema,
    customer_vehicle_service: CustomerVehicleService,
) -> CreateVehicleOwnerResponseSchema:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    vehicle_owner_response = await customer_vehicle_service.create_vehicle_owner(
        customer_id=User.customer.id,
        vehicle_owner_data=vehicle_data,
    )
    return vehicle_owner_response


async def _list_vehicles_by_customer(
    User: DepCurrentUser,
    customer_vehicle_service: CustomerVehicleService,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> ListVehicleByCustomerResponseSchema:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    vehicles_response = await customer_vehicle_service.list_vehicles_by_customer(
        customer_id=User.customer.id,
        skip=skip,
        limit=limit,
    )
    return vehicles_response


async def _delete_customer_vehicle(
    User: DepCurrentUser,
    vehicle_id: uuid.UUID,
    customer_vehicle_service: CustomerVehicleService,
) -> None:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    await customer_vehicle_service.delete_vehicle_owner(
        customer_id=User.customer.id,
        vehicle_id=str(vehicle_id),
    )


async def _get_vehicle_statistics(
    User: DepCurrentUser,
    plate: str,
    customer_vehicle_service: CustomerVehicleService,
) -> VehicleStatisticsResponseSchema:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    vehicle = await customer_vehicle_service.get_vehicle_by_plate(plate=plate)
    if not vehicle:
        raise errors.ResourceNotFound(message="Vehicle with the given plate not found")

    is_customer_owner = await customer_vehicle_service.is_customer_vehicle_owner(
        customer_id=User.customer.id,
        vehicle_id=vehicle.id,
    )
    if not is_customer_owner:
        raise errors.InvalidOperation(
            message="Customer is not the owner of this vehicle"
        )

    vehicle_statistics = await customer_vehicle_service.get_vehicle_statistics_by_id(
        vehicle_id=vehicle.id,
    )
    return vehicle_statistics


async def _list_customer_active_vehicles(
    User: DepCurrentUser,
    customer_vehicle_service: CustomerVehicleService,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> ListActiveVehiclesResponseSchema:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    active_vehicles = await customer_vehicle_service.list_active_vehicles_by_customer(
        customer_id=User.customer.id,
        skip=skip,
        limit=limit,
    )
    return active_vehicles


DepListCustomerActiveVehicles: TypeAlias = Annotated[
    ListActiveVehiclesResponseSchema,
    Depends(_list_customer_active_vehicles),
]

DepGetVehicleStatistics: TypeAlias = Annotated[
    VehicleStatisticsResponseSchema,
    Depends(_get_vehicle_statistics),
]

DepUpsertCustomerVehicle: TypeAlias = Annotated[
    CreateVehicleOwnerResponseSchema,
    Depends(_upsert_customer_vehicle),
]

DepListVehiclesByCustomer: TypeAlias = Annotated[
    ListVehicleByCustomerResponseSchema,
    Depends(_list_vehicles_by_customer),
]

DepDeleteCustomerVehicle: TypeAlias = Annotated[
    None,
    Depends(_delete_customer_vehicle),
]
