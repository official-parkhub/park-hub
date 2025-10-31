import pytest
from src.modules.shared.schemas.state import BaseStateSchema
from tests.helpers.base_schema import BaseSchema


class TestStateSchema(BaseSchema):
    @pytest.fixture(autouse=True)
    def setup(self, faker) -> None:
        self.base_state_cases = [
            (
                "Valid state",
                {"name": faker.state(), "country": "BR", "iso2_code": "DF"},
                False,
            ),
            (
                "Invalid missing iso2_code",
                {"name": faker.state(), "country": "BR"},
                True,
            ),
            (
                "Invalid country value",
                {"name": faker.state(), "country": "XX", "iso2_code": "SP"},
                True,
            ),
        ]

    def test_base_state_schema_fields(self):
        self.assert_schema_fields(
            schema=BaseStateSchema,
            expected_fields=["name", "country", "iso2_code"],
        )

    def test_base_state_schema(self):
        self.assert_multiple_params(
            data_list=self.base_state_cases, expected_schema=BaseStateSchema
        )
