import datetime
import uuid
from pydantic import AwareDatetime, BaseModel, Field

from src.modules.shared.enums.country import Country
from src.modules.shared.schemas import PaginationSchema


class BaseVehicleSchema(BaseModel):
    plate: str = Field(min_length=1, max_length=20)
    model: str | None = Field(default=None, max_length=100)
    year: int | None = Field(default=None, ge=1900, le=2100)
    color: str | None = Field(default=None, max_length=50)
    country: Country = Country.BR


class UpsertVehicleSchema(BaseVehicleSchema):
    pass


class UpsertVehicleResponseSchema(BaseVehicleSchema):
    id: uuid.UUID


class BaseVehicleOwnerSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CreateVehicleOwnerSchema(BaseVehicleOwnerSchema):
    vehicle: UpsertVehicleSchema


class CreateVehicleOwnerResponseSchema(BaseVehicleSchema):
    id: uuid.UUID
    vehicle_id: uuid.UUID


class RegisterVehicleEntranceSchema(BaseModel):
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: AwareDatetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    ended_at: AwareDatetime | None = None
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
    entrance_date: AwareDatetime
    hourly_rate: int | None


class VehicleEntranceInputSchema(BaseModel):
    plate: str = Field(min_length=1, max_length=20)


class VehicleExitResponseSchema(BaseModel):
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: AwareDatetime
    ended_at: AwareDatetime
    total_price: float
    hourly_rate: int | None


class VehicleEntranceStatisticsSchema(BaseModel):
    vehicle_id: uuid.UUID
    company_id: uuid.UUID
    entrance_date: AwareDatetime
    ended_at: AwareDatetime | None
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


class ListActiveVehiclesResponseSchema(PaginationSchema):
    data: list[VehicleEntranceStatisticsSchema]
