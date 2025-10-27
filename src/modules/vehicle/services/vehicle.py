from sqlalchemy import select

from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.driver.models.customer import Customer
from src.modules.vehicle.models.vehicle import Vehicle
from src.modules.vehicle.schemas.vehicle import (
    CreateVehicleOwnerResponseSchema,
    CreateVehicleOwnerSchema,
    RegisterVehicleEntranceResponseSchema,
    RegisterVehicleEntranceSchema,
    UpsertVehicleResponseSchema,
    UpsertVehicleSchema,
)


@dependable
class VehicleService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def upsert_vehicle(
        self,
        vehicle_data: UpsertVehicleSchema,
    ) -> UpsertVehicleResponseSchema:
        vehicle_stmt = self.db.execute(
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

    async def create_vehicle_owner(
        self,
        vehicle_owner_data: CreateVehicleOwnerSchema,
    ) -> CreateVehicleOwnerResponseSchema:
        vehicle = await self.upsert_vehicle(vehicle_owner_data.vehicle)

        vehicle_owner = Customer(
            customer_id=vehicle_owner_data.customer_id,
            name=vehicle_owner_data.name,
            vehicle_id=vehicle.id,
        )
        self.db.add(vehicle_owner)
        await self.db.flush()
        await self.db.refresh(vehicle_owner)

        return CreateVehicleOwnerResponseSchema(
            id=vehicle_owner.id,
            customer_id=vehicle_owner.customer_id,
            name=vehicle_owner.name,
            vehicle_id=vehicle.id,
        )

    async def register_vehicle_entrance(
        self,
        vehicle_entrance_data: RegisterVehicleEntranceSchema,
    ) -> RegisterVehicleEntranceResponseSchema:
        pass
