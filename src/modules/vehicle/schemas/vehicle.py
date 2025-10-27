from datetime import datetime
import uuid
from pydantic import BaseModel

from src.modules.shared.enums.country import Country


class BaseVehicleSchema(BaseModel):
    plate: str
    model: str | None = None
    year: int | None = None
    color: str | None = None
    country: Country = Country.BR


class UpsertVehicleSchema(BaseVehicleSchema):
    pass


class UpsertVehicleResponseSchema(BaseVehicleSchema):
    id: uuid.UUID


class BaseVehicleOwnerSchema(BaseModel):
    customer_id: uuid.UUID
    name: str


class CreateVehicleOwnerSchema(BaseVehicleOwnerSchema):
    vehicle: UpsertVehicleSchema


class CreateVehicleOwnerResponseSchema(BaseVehicleOwnerSchema):
    id: uuid.UUID
    vehicle_id: uuid.UUID


class RegisterVehicleEntranceSchema(BaseModel):
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: datetime = datetime.now()
    ended_at: datetime | None = None
    total_price: int | None = None
    hourly_rate: int | None = None


class RegisterVehicleEntranceResponseSchema(RegisterVehicleEntranceSchema):
    id: uuid.UUID
