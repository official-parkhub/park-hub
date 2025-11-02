from uuid import uuid4
from faker import Faker

from src.modules.shared.models.geo.city import City
from src.modules.shared.enums.country import Country


EMPTY = "empty"


class CityBuilder:
    faker = Faker()

    def __init__(self):
        self.attrs: dict = {
            "id": uuid4(),
            "name": self.faker.city(),
            "identification_code": self.faker.postcode(),
            "country": Country.BR,
            "state_id": EMPTY,
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_city(self) -> City:
        return City(**self.attrs)

    async def build(self, db) -> City:
        if self.attrs.get("state_id") == EMPTY:
            from tests.helpers.builders.state_builder import StateBuilder

            st = await StateBuilder().build(db)
            self.attrs["state_id"] = st.id

        city = City(**self.attrs)
        db.add(city)
        await db.flush()
        await db.refresh(city)
        return city
