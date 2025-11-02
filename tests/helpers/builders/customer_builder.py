from uuid import uuid4
from faker import Faker

from src.modules.driver.models.customer import Customer


EMPTY = "empty"


class CustomerBuilder:
    faker = Faker()

    def __init__(self):
        self.attrs: dict = {
            "id": uuid4(),
            "user_id": EMPTY,
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "birth_date": self.faker.date_of_birth(minimum_age=18, maximum_age=90),
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_customer(self) -> Customer:
        return Customer(**self.attrs)

    async def build(self, db) -> Customer:
        if self.attrs.get("user_id") == EMPTY:
            from tests.helpers.builders.user_builder import UserBuilder

            user = await UserBuilder().build(db)
            self.attrs["user_id"] = user.id

        cust = Customer(**self.attrs)
        db.add(cust)
        await db.flush()
        await db.refresh(cust)
        await db.commit()
        return cust
