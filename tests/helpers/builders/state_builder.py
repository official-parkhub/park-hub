from uuid import uuid4
from faker import Faker

from src.modules.shared.models.geo.state import State
from src.modules.shared.enums.country import Country


class StateBuilder:
    faker = Faker()

    def __init__(self):
        self.attrs: dict = {
            "id": uuid4(),
            "country": Country.BR,
            "name": self.faker.unique.state(),
            "iso2_code": self.faker.unique.bothify("??").upper(),
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_state(self) -> State:
        return State(**self.attrs)

    async def build(self, db) -> State:
        st = State(**self.attrs)
        db.add(st)
        await db.flush()
        await db.refresh(st)
        await db.commit()
        return st
