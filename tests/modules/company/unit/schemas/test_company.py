from src.modules.company.schemas.company.company import (
    BaseCompanySchema,
    CompleteCompanySchema,
    BaseParkingPriceSchema,
    BaseParkingExceptionSchema,
)
from src.modules.shared.schemas.city import BaseCitySchema
from src.modules.company.schemas.organization import OrganizationSchema
from src.modules.shared.schemas.state import StateWithIDSchema
from tests.helpers.base_schema import BaseSchema


class TestCompanySchemas(BaseSchema):
    def test_base_company_schema_fields(self):
        self.assert_schema_fields(
            schema=BaseCompanySchema,
            expected_fields=[
                "name",
                "postal_code",
                "register_code",
                "address",
                "description",
                "is_covered",
                "has_camera",
                "total_spots",
                "has_charging_station",
            ],
        )

    def test_complete_company_schema_nested(self, faker):
        company = CompleteCompanySchema(
            id=faker.uuid4(),
            name=faker.company(),
            postal_code=faker.postcode(),
            register_code=faker.bothify(text="##.###.###/####-##"),
            address=faker.address(),
            is_covered=faker.pybool(),
            has_camera=faker.pybool(),
            total_spots=faker.random_int(min=1, max=1000),
            has_charging_station=faker.pybool(),
            city=BaseCitySchema(
                name=faker.city(), identification_code=faker.postcode(), country="BR"
            ),
            organization_id=faker.uuid4(),
            organization=OrganizationSchema(
                id=faker.uuid4(),
                user_id=faker.uuid4(),
                name=faker.company(),
                register_code=faker.bothify(text="###########"),
                state_id=faker.uuid4(),
                state=StateWithIDSchema(
                    id=faker.uuid4(),
                    name=faker.state(),
                    country="BR",
                    iso2_code=faker.state_abbr(),
                ),
            ),
            parking_prices=[
                BaseParkingPriceSchema(
                    start_hour=faker.random_int(min=0, max=20),
                    end_hour=23,
                    price_cents=faker.random_int(min=0, max=5000),
                    is_discount=faker.pybool(),
                    week_day=faker.random_int(min=0, max=6),
                )
            ],
            parking_exceptions=[
                BaseParkingExceptionSchema(
                    start_hour=faker.random_int(min=0, max=20),
                    end_hour=23,
                    description=faker.sentence(),
                    price_cents=faker.random_int(min=0, max=5000),
                    exception_date=faker.date(),
                )
            ],
        )
        assert company.city.country.value == "BR"
        assert 1 <= company.total_spots <= 1000
