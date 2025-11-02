from datetime import datetime, timezone, date

import pytest

from src.core import errors
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.company.schemas.company.company_price import (
    CreateParkingPriceSchema,
    CreateParkingPriceExceptionSchema,
)
from tests.helpers.builders.company_builder import CompanyBuilder


class TestCompanyPriceService:
    @pytest.fixture(autouse=True)
    def setup(self, rc):
        self.service = CompanyPriceService(rc)

    async def test_create_parking_price_overlap_raises(self, db):
        company = await CompanyBuilder().build(db)

        ref_dt = datetime(2025, 1, 7, 12, 0, tzinfo=timezone.utc)
        week_day = ref_dt.weekday()

        await self.service.create_parking_price(
            str(company.id),
            CreateParkingPriceSchema(
                week_day=week_day,
                start_hour=10,
                end_hour=14,
                price_cents=1200,
                is_discount=False,
            ),
        )

        with pytest.raises(errors.InvalidOperation):
            await self.service.create_parking_price(
                str(company.id),
                CreateParkingPriceSchema(
                    week_day=week_day,
                    start_hour=12,
                    end_hour=16,
                    price_cents=1100,
                    is_discount=False,
                ),
            )

    async def test_get_reference_returns_none_when_no_prices(self, db):
        company = await CompanyBuilder().build(db)
        ref = await self.service.get_parking_price_reference(str(company.id))
        assert ref is None

    async def test_duplicate_exception_same_date_raises(self, db):
        company = await CompanyBuilder().build(db)

        exc_date = date(2025, 1, 9)
        await self.service.create_parking_price_exception(
            str(company.id),
            CreateParkingPriceExceptionSchema(
                start_hour=8,
                end_hour=12,
                price_cents=700,
                is_discount=False,
                description=None,
                exception_date=exc_date,
            ),
        )

        with pytest.raises(errors.InvalidOperation):
            await self.service.create_parking_price_exception(
                str(company.id),
                CreateParkingPriceExceptionSchema(
                    start_hour=10,
                    end_hour=14,
                    price_cents=600,
                    is_discount=True,
                    description="dup",
                    exception_date=exc_date,
                ),
            )

    async def test_exception_overrides_regular_price_in_reference(self, db):
        company = await CompanyBuilder().build(db)
        # Regular price for Wednesday 12h
        ref_dt = datetime(
            2025, 1, 8, 12, 0, tzinfo=timezone.utc
        )  # 2025-01-08 is a Wednesday
        week_day = ref_dt.weekday()
        await self.service.create_parking_price(
            str(company.id),
            CreateParkingPriceSchema(
                week_day=week_day,
                start_hour=10,
                end_hour=14,
                price_cents=1200,
                is_discount=False,
            ),
        )

        # Exception on that date should take precedence with cheaper price
        await self.service.create_parking_price_exception(
            str(company.id),
            CreateParkingPriceExceptionSchema(
                start_hour=8,
                end_hour=18,
                price_cents=700,
                is_discount=False,
                description=None,
                exception_date=ref_dt.date(),
            ),
        )

        ref = await self.service.get_parking_price_reference(
            str(company.id), reference_datetime=ref_dt
        )
        assert ref is not None
        assert ref.price_cents == 700
