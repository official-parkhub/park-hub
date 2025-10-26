from sqlalchemy import select

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.company.models.parking_price import ParkingPrice
from src.modules.company.schemas.company.company_price import (
    CreateParkingPriceResponseSchema,
    CreateParkingPriceSchema,
)
from src.utils.time_overlap import interval_overlap


@dependable
class CompanyPriceService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def create_parking_price(
        self, parking_price_schema: CreateParkingPriceSchema
    ) -> CreateParkingPriceResponseSchema:
        if parking_price_schema.week_day < 0 or parking_price_schema.week_day > 6:
            raise errors.InvalidOperationError(
                message="week_day must be between 0 (Monday) and 6 (Sunday)"
            )

        existing_parking_price_stmt = await self.db.execute(
            select(ParkingPrice).where(
                ParkingPrice.company_id == parking_price_schema.company_id,
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
            company_id=parking_price_schema.company_id,
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
