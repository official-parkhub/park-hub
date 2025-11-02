from uuid import uuid4
from datetime import datetime, timedelta, timezone
from faker import Faker

from src.modules.vehicle.models.vehicle_entrance import VehicleEntrance


EMPTY = "empty"


class VehicleEntranceBuilder:
    faker = Faker()

    def __init__(self):
        now = datetime.now(timezone.utc)
        self.attrs: dict = {
            "id": uuid4(),
            "vehicle_id": EMPTY,
            "company_id": EMPTY,
            "entrance_date": now - timedelta(hours=self.faker.random_int(0, 4)),
            "ended_at": None,
            "hourly_rate": self.faker.random_int(min=500, max=5000),
            "total_price": None,
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_vehicle_entrance(self) -> VehicleEntrance:
        return VehicleEntrance(**self.attrs)

    async def build(self, db) -> VehicleEntrance:
        if self.attrs.get("vehicle_id") == EMPTY:
            from tests.helpers.builders.vehicle_builder import VehicleBuilder

            v = await VehicleBuilder().build(db)
            self.attrs["vehicle_id"] = v.id

        if self.attrs.get("company_id") == EMPTY:
            from tests.helpers.builders.company_builder import CompanyBuilder

            c = await CompanyBuilder().build(db)
            self.attrs["company_id"] = c.id

        ve = VehicleEntrance(**self.attrs)
        db.add(ve)
        await db.flush()
        await db.refresh(ve)
        await db.commit()
        return ve
