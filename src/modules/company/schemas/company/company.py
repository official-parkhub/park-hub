from datetime import datetime
from pydantic import BaseModel
import uuid

from src.modules.company.schemas.organization import OrganizationSchema
from src.modules.shared.schemas import PaginationSchema
from src.modules.shared.schemas.city import BaseCitySchema


class BaseCompanyImageSchema(BaseModel):
    id: uuid.UUID
    url: str
    is_primary: bool


class BaseParkingPriceSchema(BaseModel):
    start_hour: int
    end_hour: int
    price_cents: int
    is_discount: bool
    week_day: int | None = None


class ParkingPriceWithIDSchema(BaseParkingPriceSchema):
    id: uuid.UUID


class BaseParkingExceptionSchema(BaseModel):
    start_hour: int
    end_hour: int
    description: str
    price_cents: int
    exception_date: datetime


class ParkingExceptionWithIDSchema(BaseParkingExceptionSchema):
    id: uuid.UUID


class BaseCompanySchema(BaseModel):
    name: str
    postal_code: str
    register_code: str
    address: str
    description: str | None = None
    is_covered: bool
    has_camera: bool
    total_spots: int
    has_charging_station: bool


class CompanyWithTodayPricesSchema(BaseCompanySchema):
    id: uuid.UUID
    city: BaseCitySchema
    images: list[BaseCompanyImageSchema] = []
    today_parking_price: BaseParkingPriceSchema | None = None


class CompanyListResponseSchema(PaginationSchema):
    data: list[CompanyWithTodayPricesSchema]


class CompleteCompanySchema(BaseCompanySchema):
    id: uuid.UUID
    city: BaseCitySchema
    organization_id: uuid.UUID
    organization: OrganizationSchema
    parking_prices: list[BaseParkingPriceSchema]
    parking_exceptions: list[BaseParkingExceptionSchema]
