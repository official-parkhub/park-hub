from typing import Annotated

from fastapi import Depends
from src.core import errors
from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.vehicle.schemas.vehicle import (
    CreateVehicleOwnerResponseSchema,
    CreateVehicleOwnerSchema,
    ListVehicleByCustomerResponseSchema,
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
    skip: int = 0,
    limit: int = 10,
) -> ListVehicleByCustomerResponseSchema:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    vehicles_response = await customer_vehicle_service.list_vehicles_by_customer(
        customer_id=User.customer.id,
        skip=skip,
        limit=limit,
    )
    return vehicles_response


DepUpsertCustomerVehicle = Annotated[
    CreateVehicleOwnerResponseSchema,
    Depends(_upsert_customer_vehicle),
]

DepListVehiclesByCustomer = Annotated[
    ListVehicleByCustomerResponseSchema,
    Depends(_list_vehicles_by_customer),
]
