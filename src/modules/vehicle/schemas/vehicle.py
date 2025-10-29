from datetime import datetime
import uuid
from pydantic import BaseModel

from src.modules.shared.enums.country import Country
from src.modules.shared.schemas import PaginationSchema


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
    name: str


class CreateVehicleOwnerSchema(BaseVehicleOwnerSchema):
    vehicle: UpsertVehicleSchema


class CreateVehicleOwnerResponseSchema(BaseVehicleSchema):
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


class ListVehicleByCustomerItemSchema(BaseVehicleSchema):
    vehicle_id: uuid.UUID
    name_given_by_owner: str


class ListVehicleByCustomerResponseSchema(PaginationSchema):
    vehicles: list[ListVehicleByCustomerItemSchema]
