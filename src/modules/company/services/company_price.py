from datetime import datetime, timezone
from sqlalchemy import select

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.company.models.parking_exception import ParkingException
from src.modules.company.models.parking_price import ParkingPrice
from src.modules.company.schemas.company.company_price import (
    CreateParkingPriceExceptionResponseSchema,
    CreateParkingPriceExceptionSchema,
    CreateParkingPriceResponseSchema,
    CreateParkingPriceSchema,
    ListParkingPricesResponseSchema,
    ParkingPriceReferenceSchema,
)
from src.modules.company.schemas.company.company import BaseParkingPriceSchema
from src.utils.time_overlap import interval_overlap


@dependable
class CompanyPriceService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def create_parking_price(
        self, company_id: str, parking_price_schema: CreateParkingPriceSchema
    ) -> CreateParkingPriceResponseSchema:
        if parking_price_schema.week_day < 0 or parking_price_schema.week_day > 6:
            raise errors.InvalidOperationError(
                message="week_day must be between 0 (Monday) and 6 (Sunday)"
            )

        existing_parking_price_stmt = await self.db.execute(
            select(ParkingPrice).where(
                ParkingPrice.company_id == company_id,
                ParkingPrice.week_day == parking_price_schema.week_day,
            ),
        )
        existing_parking_price = existing_parking_price_stmt.scalars()

        for parking_price in existing_parking_price:
            if interval_overlap(
                parking_price.start_hour,
                parking_price.end_hour,
                parking_price_schema.start_hour,
                parking_price_schema.end_hour,
            ):
                raise errors.InvalidOperation(
                    message="Parking price time range overlaps with an existing price for the same day"
                )

        db_parking_price = ParkingPrice(
            company_id=company_id,
            week_day=parking_price_schema.week_day,
            start_hour=parking_price_schema.start_hour,
            end_hour=parking_price_schema.end_hour,
            price_cents=parking_price_schema.price_cents,
            is_discount=parking_price_schema.is_discount,
        )
        self.db.add(db_parking_price)
        await self.db.flush()
        await self.db.refresh(db_parking_price)
        return CreateParkingPriceResponseSchema.model_validate(
            db_parking_price, from_attributes=True
        )

    async def create_parking_price_exception(
        self,
        company_id: str,
        create_parking_price_exception_schema: CreateParkingPriceExceptionSchema,
    ) -> CreateParkingPriceExceptionResponseSchema:
        existing_exception_stmt = await self.db.execute(
            select(ParkingException).where(
                ParkingException.company_id == company_id,
                ParkingException.exception_date
                == create_parking_price_exception_schema.exception_date,
                ParkingException.active,
            ),
        )
        existing_exception = existing_exception_stmt.scalars().first()

        if existing_exception:
            raise errors.InvalidOperation(
                message="Parking price exception already exists for this date"
            )

        db_parking_exception = ParkingException(
            company_id=company_id,
            start_hour=create_parking_price_exception_schema.start_hour,
            end_hour=create_parking_price_exception_schema.end_hour,
            price_cents=create_parking_price_exception_schema.price_cents,
            is_discount=create_parking_price_exception_schema.is_discount,
            description=create_parking_price_exception_schema.description,
            exception_date=create_parking_price_exception_schema.exception_date,
        )
        self.db.add(db_parking_exception)
        await self.db.flush()
        await self.db.refresh(db_parking_exception)
        return CreateParkingPriceExceptionResponseSchema.model_validate(
            db_parking_exception, from_attributes=True
        )

    async def get_parking_price_reference(
        self,
        company_id: str,
        reference_datetime: datetime = datetime.now(timezone.utc),
    ) -> ParkingPriceReferenceSchema | None:
        exception_stmt = await self.db.execute(
            select(ParkingException)
            .where(
                ParkingException.company_id == company_id,
                ParkingException.exception_date == reference_datetime.date(),
                ParkingException.active,
            )
            .order_by(ParkingException.price_cents.asc())
            .limit(1)
        )
        parking_exception = exception_stmt.scalars().first()

        if parking_exception:
            return ParkingPriceReferenceSchema.model_validate(
                parking_exception, from_attributes=True
            )

        day_of_week = reference_datetime.weekday()
        hour_of_day = reference_datetime.hour

        result = await self.db.execute(
            select(ParkingPrice)
            .where(
                ParkingPrice.company_id == company_id,
                ParkingPrice.week_day == day_of_week,
                ParkingPrice.start_hour <= hour_of_day,
                ParkingPrice.end_hour >= hour_of_day,
            )
            .order_by(ParkingPrice.price_cents.asc())
            .limit(1)
        )

        parking_price = result.scalars().first()
        if not parking_price:
            return None

        return ParkingPriceReferenceSchema.model_validate(
            parking_price, from_attributes=True
        )

    async def list_parking_prices(
        self,
        company_id: str,
    ) -> ListParkingPricesResponseSchema:
        result = await self.db.execute(
            select(ParkingPrice).where(
                ParkingPrice.company_id == company_id,
                ParkingPrice.active,
            )
        )
        parking_prices = result.scalars().all()
        total = len(parking_prices)
        return ListParkingPricesResponseSchema(
            total=total,
            skip=0,
            limit=total,
            data=[
                BaseParkingPriceSchema.model_validate(price, from_attributes=True)
                for price in parking_prices
            ],
        )
