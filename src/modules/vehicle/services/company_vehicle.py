from datetime import datetime
import math
from sqlalchemy import literal_column, select

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.vehicle.models.vehicle import Vehicle
from src.modules.vehicle.models.vehicle_entrance import VehicleEntrance
from src.modules.vehicle.schemas.vehicle import (
    ListActiveVehiclesResponseSchema,
    VehicleEntranceResponseSchema,
    VehicleEntranceStatisticsSchema,
    VehicleExitResponseSchema,
)


@dependable
class CompanyVehicleService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def register_vehicle_entrance(
        self,
        company_price_service: CompanyPriceService,
        company_id: str,
        vehicle_id: str,
    ) -> VehicleEntranceResponseSchema:
        vehicle_stmt = await self.db.execute(
            select(Vehicle).where(
                Vehicle.id == vehicle_id,
                Vehicle.active,
            )
        )
        vehicle = vehicle_stmt.scalar_one_or_none()

        if not vehicle:
            raise errors.ResourceNotFound(message="Vehicle not found")

        parking_price_reference = (
            await company_price_service.get_parking_price_reference(
                company_id=company_id,
            )
        )

        if not parking_price_reference:
            raise errors.ResourceNotFound(
                message="No parking prices found for the company"
            )

        vehicle_entrance = VehicleEntrance(
            vehicle_id=vehicle.id,
            company_id=company_id,
            hourly_rate=parking_price_reference.price_cents,
        )
        self.db.add(vehicle_entrance)
        await self.db.flush()
        return VehicleEntranceResponseSchema.model_validate(
            vehicle_entrance, from_attributes=True
        )

    async def get_active_vehicle_entrance(
        self,
        vehicle_id: str,
        company_id: str,
    ) -> VehicleEntranceResponseSchema | None:
        vehicle_entrance_stmt = await self.db.execute(
            select(VehicleEntrance).where(
                VehicleEntrance.vehicle_id == vehicle_id,
                VehicleEntrance.ended_at.is_(None),
                VehicleEntrance.company_id == company_id,
                VehicleEntrance.active,
            )
        )
        vehicle_entrance = vehicle_entrance_stmt.scalar_one_or_none()

        if not vehicle_entrance:
            return None

        return VehicleEntranceResponseSchema.model_validate(
            vehicle_entrance, from_attributes=True
        )

    async def register_vehicle_exit(
        self,
        vehicle_entrance_id: str,
        ended_at: datetime,
    ) -> VehicleExitResponseSchema:
        vehicle_entrance_stmt = await self.db.execute(
            select(VehicleEntrance).where(
                VehicleEntrance.id == vehicle_entrance_id,
                VehicleEntrance.ended_at.is_(None),
                VehicleEntrance.active,
            )
        )
        vehicle_entrance = vehicle_entrance_stmt.scalar_one_or_none()

        if not vehicle_entrance:
            raise errors.ResourceNotFound(message="Active vehicle entrance not found")

        vehicle_entrance.ended_at = ended_at
        vehicle_entrance.total_price = math.floor(
            ((ended_at - vehicle_entrance.entrance_date).total_seconds() / 3600)
            * vehicle_entrance.hourly_rate
        )
        self.db.add(vehicle_entrance)
        await self.db.flush()
        return VehicleExitResponseSchema.model_validate(
            vehicle_entrance, from_attributes=True
        )

    async def list_active_vehicles_by_company(
        self,
        company_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ListActiveVehiclesResponseSchema]:
        vehicle_entrance_stmt = await self.db.execute(
            select(
                VehicleEntrance.id,
                VehicleEntrance.active,
                VehicleEntrance.vehicle_id,
                VehicleEntrance.company_id,
                VehicleEntrance.entrance_date,
                VehicleEntrance.ended_at,
                VehicleEntrance.hourly_rate,
                VehicleEntrance.total_price,
                Vehicle.plate.label("plate"),
            )
            .join(Vehicle, Vehicle.id == VehicleEntrance.vehicle_id)
            .where(
                VehicleEntrance.company_id == company_id,
                VehicleEntrance.ended_at.is_(None),
                VehicleEntrance.active,
            )
            .offset(skip)
            .limit(limit)
        )
        vehicle_entrances = vehicle_entrance_stmt.all()

        vehicle_entrances_count_stmt = await self.db.execute(
            select(literal_column("COUNT(*)")).where(
                VehicleEntrance.company_id == company_id,
                VehicleEntrance.ended_at.is_(None),
                VehicleEntrance.active,
            )
        )
        vehicle_entrances_count = vehicle_entrances_count_stmt.scalar_one_or_none()

        return ListActiveVehiclesResponseSchema(
            total=vehicle_entrances_count,
            skip=skip,
            limit=limit,
            data=[
                VehicleEntranceStatisticsSchema.model_validate(
                    vehicle_entrance, from_attributes=True
                )
                for vehicle_entrance in vehicle_entrances
            ],
        )

    async def list_vehicles_by_company(
        self,
        company_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ListActiveVehiclesResponseSchema]:
        vehicle_entrance_stmt = await self.db.execute(
            select(
                VehicleEntrance.id,
                VehicleEntrance.active,
                VehicleEntrance.vehicle_id,
                VehicleEntrance.company_id,
                VehicleEntrance.entrance_date,
                VehicleEntrance.ended_at,
                VehicleEntrance.hourly_rate,
                VehicleEntrance.total_price,
                Vehicle.plate.label("plate"),
            )
            .join(Vehicle, Vehicle.id == VehicleEntrance.vehicle_id)
            .where(
                VehicleEntrance.company_id == company_id,
                VehicleEntrance.active,
            )
            .order_by(VehicleEntrance.entrance_date.desc())
            .limit(limit)
            .offset(skip)
        )
        vehicle_entrances = vehicle_entrance_stmt.all()

        vehicle_entrances_count_stmt = await self.db.execute(
            select(literal_column("COUNT(*)")).where(
                VehicleEntrance.company_id == company_id,
                VehicleEntrance.active,
            )
        )
        vehicle_entrances_count = vehicle_entrances_count_stmt.scalar_one_or_none()

        return ListActiveVehiclesResponseSchema(
            total=vehicle_entrances_count,
            skip=skip,
            limit=limit,
            data=[
                VehicleEntranceStatisticsSchema.model_validate(
                    vehicle_entrance, from_attributes=True
                )
                for vehicle_entrance in vehicle_entrances
            ],
        )
