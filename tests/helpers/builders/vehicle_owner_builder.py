from uuid import uuid4
from faker import Faker

from src.modules.vehicle.models.vehicle_owner import VehicleOwner


EMPTY = "empty"


class VehicleOwnerBuilder:
    faker = Faker()

    def __init__(self):
        self.attrs: dict = {
            "id": uuid4(),
            "name": self.faker.name(),
            "vehicle_id": EMPTY,  # relationship
            "customer_id": EMPTY,  # relationship
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_vehicle_owner(self) -> VehicleOwner:
        return VehicleOwner(**self.attrs)

    async def build(self, db) -> VehicleOwner:
        if self.attrs.get("vehicle_id") == EMPTY:
            from tests.helpers.builders.vehicle_builder import VehicleBuilder

            v = await VehicleBuilder().build(db)
            self.attrs["vehicle_id"] = v.id

        if self.attrs.get("customer_id") == EMPTY:
            from tests.helpers.builders.customer_builder import CustomerBuilder

            c = await CustomerBuilder().build(db)
            self.attrs["customer_id"] = c.id

        vo = VehicleOwner(**self.attrs)
        db.add(vo)
        await db.flush()
        await db.refresh(vo)
        return vo
