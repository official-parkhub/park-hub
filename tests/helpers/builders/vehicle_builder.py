from uuid import uuid4
from faker import Faker

from src.modules.shared.enums.country import Country
from src.modules.vehicle.models.vehicle import Vehicle


class VehicleBuilder:
    faker = Faker()

    def __init__(self):
        plate_pattern = self.faker.bothify(text="???-####").upper()
        self.attrs: dict = {
            "id": uuid4(),
            "plate": plate_pattern,
            "model": self.faker.word().title(),
            "year": self.faker.random_int(min=1995, max=2025),
            "color": self.faker.color_name(),
            "country": Country.BR,
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_vehicle(self) -> Vehicle:
        return Vehicle(**self.attrs)

    async def build(self, db) -> Vehicle:
        v = Vehicle(**self.attrs)
        db.add(v)
        await db.flush()
        await db.refresh(v)
        return v
