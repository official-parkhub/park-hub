import datetime
import uuid
from pydantic import AwareDatetime, BaseModel, Field

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
    entrance_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    ended_at: datetime.datetime | None = None
    total_price: int | None = None
    hourly_rate: int | None = None


class RegisterVehicleEntranceResponseSchema(RegisterVehicleEntranceSchema):
    id: uuid.UUID


class ListVehicleByCustomerItemSchema(BaseVehicleSchema):
    vehicle_id: uuid.UUID
    name_given_by_owner: str


class ListVehicleByCustomerResponseSchema(PaginationSchema):
    vehicles: list[ListVehicleByCustomerItemSchema]


class VehicleEntranceResponseSchema(BaseModel):
    id: uuid.UUID
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: datetime.datetime
    hourly_rate: int | None


class VehicleEntranceInputSchema(BaseModel):
    plate: str


class VehicleExitResponseSchema(BaseModel):
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: datetime.datetime
    ended_at: datetime.datetime
    total_price: float
    hourly_rate: int | None


class VehicleEntranceStatisticsSchema(BaseModel):
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: datetime.datetime
    ended_at: datetime.datetime | None
    total_price: float | None
    hourly_rate: int | None


class VehicleExitInputSchema(BaseModel):
    plate: str
    ended_at: AwareDatetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class GetVehicleOutput(BaseVehicleSchema):
    id: uuid.UUID


class VehicleStatisticsResponseSchema(PaginationSchema):
    vehicle: BaseVehicleSchema
    entrances: list[VehicleEntranceStatisticsSchema]
