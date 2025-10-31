import pytest
from src.modules.shared.schemas.city import BaseCitySchema
from tests.helpers.base_schema import BaseSchema


class TestCitySchema(BaseSchema):
    @pytest.fixture(autouse=True)
    def setup(self, faker) -> None:
        self.base_city_schema = [
            (
                "Valid city data",
                {
                    "name": faker.city(),
                    "identification_code": faker.postcode(),
                    "country": "BR",
                },
                False,
            ),
            (
                "Valid without identification_code",
                {"name": faker.city(), "country": "BR"},
                False,
            ),
            (
                "Invalid missing name",
                {"identification_code": faker.postcode(), "country": "BR"},
                True,
            ),
            (
                "Invalid country value",
                {
                    "name": faker.city(),
                    "identification_code": faker.postcode(),
                    "country": "XX",
                },
                True,
            ),
        ]

    def test_base_city_schema_fields(self):
        self.assert_schema_fields(
            schema=BaseCitySchema,
            expected_fields=[
                "name",
                "identification_code",
                "country",
            ],
        )

    def test_base_city_schema(self):
        self.assert_multiple_params(
            data_list=self.base_city_schema,
            expected_schema=BaseCitySchema,
        )
