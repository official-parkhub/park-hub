from datetime import date, datetime, timezone
import uuid

from pydantic import BaseModel, Field, AwareDatetime

from src.modules.company.schemas.company.company import (
    BaseCompanyImageSchema,
    BaseCompanySchema,
    BaseParkingPriceSchema,
)
from src.modules.shared.schemas import PaginationSchema
from src.modules.shared.schemas.city import BaseCitySchema


class CreateParkingPriceSchema(BaseParkingPriceSchema):
    pass


class CreateParkingPriceResponseSchema(BaseParkingPriceSchema):
    id: uuid.UUID


class BaseParkingPriceExceptionSchema(BaseModel):
    start_hour: int = Field(..., ge=0, le=23)
    end_hour: int = Field(..., ge=0, le=23)
    price_cents: int = Field(..., ge=0)
    is_discount: bool
    description: str | None = None
    exception_date: date


class CreateParkingPriceExceptionSchema(BaseParkingPriceExceptionSchema):
    pass


class CreateParkingPriceExceptionResponseSchema(BaseParkingPriceExceptionSchema):
    id: uuid.UUID


class ParkingPriceReferenceSchema(BaseModel):
    id: uuid.UUID
    start_hour: int
    end_hour: int
    price_cents: int
    is_discount: bool
    description: str | None = None
    exception_date: date | None = None
    reference_date: AwareDatetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CompanyWithTodayPricesSchema(BaseCompanySchema):
    id: uuid.UUID
    city: BaseCitySchema
    images: list[BaseCompanyImageSchema] = []
    today_parking_price: ParkingPriceReferenceSchema | None = None


class CompanyListResponseSchema(PaginationSchema):
    data: list[CompanyWithTodayPricesSchema]


class ListParkingPricesResponseSchema(PaginationSchema):
    data: list[BaseParkingPriceSchema]
