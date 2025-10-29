from sqlalchemy import select, literal_column

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.vehicle.models.vehicle import Vehicle
from src.modules.vehicle.models.vehicle_owner import VehicleOwner
from src.modules.vehicle.schemas.vehicle import (
    CreateVehicleOwnerResponseSchema,
    CreateVehicleOwnerSchema,
    ListVehicleByCustomerItemSchema,
    ListVehicleByCustomerResponseSchema,
    UpsertVehicleResponseSchema,
    UpsertVehicleSchema,
)


@dependable
class CustomerVehicleService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def upsert_vehicle(
        self,
        vehicle_data: UpsertVehicleSchema,
    ) -> UpsertVehicleResponseSchema:
        vehicle_stmt = await self.db.execute(
            select(Vehicle).where(Vehicle.plate == vehicle_data.plate)
        )
        vehicle = vehicle_stmt.scalars().first()

        if vehicle:
            return UpsertVehicleResponseSchema.model_validate(
                vehicle, from_attributes=True
            )

        vehicle = Vehicle(
            plate=vehicle_data.plate,
            model=vehicle_data.model,
            year=vehicle_data.year,
            color=vehicle_data.color,
            country=vehicle_data.country,
        )
        self.db.add(vehicle)
        await self.db.flush()
        await self.db.refresh(vehicle)
        return UpsertVehicleResponseSchema.model_validate(vehicle, from_attributes=True)

    async def is_customer_vehicle_owner(
        self,
        customer_id: str,
        vehicle_id: str,
    ) -> bool:
        vehicle_owner_stmt = await self.db.execute(
            select(VehicleOwner).where(
                VehicleOwner.customer_id == customer_id,
                VehicleOwner.vehicle_id == vehicle_id,
                VehicleOwner.active,
            )
        )
        vehicle_owner = vehicle_owner_stmt.scalars().first()

        return vehicle_owner is not None

    async def create_vehicle_owner(
        self,
        customer_id: str,
        vehicle_owner_data: CreateVehicleOwnerSchema,
    ) -> CreateVehicleOwnerResponseSchema:
        vehicle = await self.upsert_vehicle(vehicle_owner_data.vehicle)

        if await self.is_customer_vehicle_owner(
            customer_id=customer_id,
            vehicle_id=vehicle.id,
        ):
            raise errors.InvalidOperation(
                message="Customer is already the owner of this vehicle"
            )

        vehicle_owner = VehicleOwner(
            customer_id=customer_id,
            name=vehicle_owner_data.name,
            vehicle_id=vehicle.id,
        )
        self.db.add(vehicle_owner)
        await self.db.flush()
        await self.db.refresh(vehicle_owner)

        return CreateVehicleOwnerResponseSchema(
            id=str(vehicle_owner.id),
            vehicle_id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            year=vehicle.year,
            color=vehicle.color,
            country=vehicle.country,
        )

    async def list_vehicles_by_customer(
        self,
        customer_id: str,
        limit: int = 10,
        skip: int = 0,
    ) -> ListVehicleByCustomerResponseSchema:
        list_vehicles_stmt = await self.db.execute(
            select(
                VehicleOwner.customer_id,
                VehicleOwner.vehicle_id,
                VehicleOwner.name.label("name_given_by_owner"),
                Vehicle.plate,
                Vehicle.model,
                Vehicle.year,
                Vehicle.color,
                Vehicle.country,
            )
            .join(Vehicle, Vehicle.id == VehicleOwner.vehicle_id)
            .where(
                VehicleOwner.customer_id == customer_id,
                VehicleOwner.active,
            )
            .limit(limit)
            .offset(skip)
        )

        vehicles = list_vehicles_stmt.all()

        vehicles_count_stmt = await self.db.execute(
            select(literal_column("COUNT(*)"))
            .select_from(VehicleOwner)
            .where(
                VehicleOwner.customer_id == customer_id,
                VehicleOwner.active,
            )
        )

        total_vehicles = vehicles_count_stmt.scalar_one()
        return ListVehicleByCustomerResponseSchema(
            total=total_vehicles,
            limit=limit,
            skip=skip,
            vehicles=[
                ListVehicleByCustomerItemSchema(
                    vehicle_id=vehicle.vehicle_id,
                    name_given_by_owner=vehicle.name_given_by_owner,
                    plate=vehicle.plate,
                    model=vehicle.model,
                    year=vehicle.year,
                    color=vehicle.color,
                    country=vehicle.country,
                )
                for vehicle in vehicles
            ],
        )
