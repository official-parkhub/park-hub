from datetime import timezone

from src.modules.company.schemas.company.company import BaseParkingPriceSchema
from src.modules.company.schemas.company.company_price import (
    BaseParkingPriceExceptionSchema,
    CreateParkingPriceSchema,
    ParkingPriceReferenceSchema,
)
from tests.helpers.base_schema import BaseSchema


class TestCompanyPriceSchemas(BaseSchema):
    def test_base_parking_price_schema_fields(self):
        self.assert_schema_fields(
            schema=BaseParkingPriceSchema,
            expected_fields=[
                "start_hour",
                "end_hour",
                "price_cents",
                "is_discount",
                "week_day",
            ],
        )

    def test_base_parking_price_schema_valid(self, faker):
        start = faker.random_int(min=0, max=20)
        end = faker.random_int(min=start + 1, max=23)
        data = {
            "start_hour": start,
            "end_hour": end,
            "price_cents": faker.random_int(min=0, max=100_000),
            "is_discount": faker.pybool(),
            "week_day": faker.random_int(min=0, max=6),
        }
        self.assert_params(data=data, expected_schema=BaseParkingPriceSchema)

    def test_base_parking_price_schema_invalid_start(self, faker):
        base = {
            "start_hour": -1,
            "end_hour": 10,
            "price_cents": faker.random_int(min=0, max=100_000),
            "is_discount": faker.pybool(),
            "week_day": 0,
        }
        self.assert_params(
            data=base, expected_schema=BaseParkingPriceSchema, is_error=True
        )

    def test_base_parking_price_schema_invalid_end(self, faker):
        base = {
            "start_hour": 0,
            "end_hour": 24,
            "price_cents": faker.random_int(min=0, max=100_000),
            "is_discount": faker.pybool(),
            "week_day": 0,
        }
        self.assert_params(
            data=base, expected_schema=BaseParkingPriceSchema, is_error=True
        )

    def test_base_parking_price_schema_invalid_price(self, faker):
        base = {
            "start_hour": 0,
            "end_hour": 1,
            "price_cents": -1,
            "is_discount": faker.pybool(),
            "week_day": 0,
        }
        self.assert_params(
            data=base, expected_schema=BaseParkingPriceSchema, is_error=True
        )

    def test_base_parking_price_schema_invalid_weekday(self, faker):
        base = {
            "start_hour": 0,
            "end_hour": 1,
            "price_cents": faker.random_int(min=0, max=100_000),
            "is_discount": faker.pybool(),
            "week_day": 7,
        }
        self.assert_params(
            data=base, expected_schema=BaseParkingPriceSchema, is_error=True
        )

    def test_create_parking_price_schema_alias(self, faker):
        valid = {
            "start_hour": faker.random_int(min=0, max=22),
            "end_hour": 23,
            "price_cents": faker.random_int(min=0, max=10_000),
            "is_discount": faker.pybool(),
            "week_day": faker.random_int(min=0, max=6),
        }
        self.assert_params(data=valid, expected_schema=CreateParkingPriceSchema)

    def test_base_parking_price_exception_schema(self):
        self.assert_schema_fields(
            schema=BaseParkingPriceExceptionSchema,
            expected_fields=[
                "start_hour",
                "end_hour",
                "price_cents",
                "is_discount",
                "description",
                "exception_date",
            ],
        )

    def test_parking_price_reference_schema_defaults_timezone(self, faker):
        ref = ParkingPriceReferenceSchema(
            id=faker.uuid4(),
            start_hour=faker.random_int(min=0, max=22),
            end_hour=23,
            price_cents=faker.random_int(min=0, max=10_000),
            is_discount=faker.pybool(),
        )
        assert ref.reference_date.tzinfo is not None
        assert ref.reference_date.tzinfo == timezone.utc
