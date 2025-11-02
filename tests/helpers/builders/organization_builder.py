from uuid import uuid4
from faker import Faker

from src.modules.company.models.organization import Organization


EMPTY = "empty"


class OrganizationBuilder:
    faker = Faker()

    def __init__(self):
        self.attrs: dict = {
            "id": uuid4(),
            "user_id": EMPTY,  # relationship -> build if empty
            "name": self.faker.company(),
            "register_code": self.faker.unique.msisdn(),
            "state_id": EMPTY,  # relationship -> build if empty
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_organization(self) -> Organization:
        return Organization(**self.attrs)

    async def build(self, db) -> Organization:
        # resolve relationships lazily
        if self.attrs.get("user_id") == EMPTY:
            from tests.helpers.builders.user_builder import UserBuilder

            user = await UserBuilder().build(db)
            self.attrs["user_id"] = user.id

        if self.attrs.get("state_id") == EMPTY:
            from tests.helpers.builders.state_builder import StateBuilder

            state = await StateBuilder().build(db)
            self.attrs["state_id"] = state.id

        org = Organization(**self.attrs)
        db.add(org)
        await db.flush()
        await db.refresh(org)
        return org
