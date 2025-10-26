from pydantic import BaseModel
import uuid

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


class BaseCompanySchema(BaseModel):
    name: str
    postal_code: str
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
