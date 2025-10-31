from datetime import timezone

from src.modules.vehicle.schemas.vehicle import (
    BaseVehicleSchema,
    VehicleExitInputSchema,
    RegisterVehicleEntranceSchema,
)
from tests.helpers.base_schema import BaseSchema


class TestVehicleSchemas(BaseSchema):
    def test_base_vehicle_schema_fields(self):
        self.assert_schema_fields(
            schema=BaseVehicleSchema,
            expected_fields=["plate", "model", "year", "color", "country"],
        )

    def test_base_vehicle_validation(self, faker):
        valid = {"plate": faker.bothify(text="???####").upper(), "country": "BR"}
        self.assert_params(
            data=valid, expected_schema=BaseVehicleSchema, is_error=False
        )

        invalid_empty_plate = {"plate": "", "country": "BR"}
        self.assert_params(
            data=invalid_empty_plate, expected_schema=BaseVehicleSchema, is_error=True
        )

        valid_long_plate = {
            "plate": faker.pystr(min_chars=7, max_chars=12),
            "country": "BR",
        }
        self.assert_params(
            data=valid_long_plate, expected_schema=BaseVehicleSchema, is_error=False
        )

        invalid_country = {
            "plate": faker.bothify(text="???-####").upper(),
            "country": "XX",
        }
        self.assert_params(
            data=invalid_country, expected_schema=BaseVehicleSchema, is_error=True
        )

    def test_vehicle_exit_input_default_aware(self, faker):
        schema = VehicleExitInputSchema(plate=faker.bothify(text="???####").upper())
        assert schema.ended_at.tzinfo is not None
        assert schema.ended_at.tzinfo == timezone.utc

    def test_register_vehicle_entrance_schema_dates(self, faker):
        s = RegisterVehicleEntranceSchema(
            vehicle_id=faker.uuid4(),
            company_id=faker.uuid4(),
        )
        assert s.entrance_date.tzinfo == timezone.utc
