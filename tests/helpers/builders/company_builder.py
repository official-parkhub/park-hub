from uuid import uuid4
from faker import Faker

from src.modules.company.models.company import Company


EMPTY = "empty"


class CompanyBuilder:
    faker = Faker()

    def __init__(self):
        self.attrs: dict = {
            "id": uuid4(),
            "organization_id": EMPTY,  # relationship -> build if empty
            "city_id": EMPTY,  # relationship -> build if empty
            "name": self.faker.company(),
            "register_code": self.faker.unique.ean(length=13),
            "address": self.faker.street_address(),
            "postal_code": self.faker.postcode(),
            "description": self.faker.sentence(nb_words=6),
            "is_covered": self.faker.boolean(),
            "has_camera": self.faker.boolean(),
            "total_spots": self.faker.random_int(min=5, max=50),
            "has_charging_station": self.faker.boolean(),
        }

    def customize(self, **kwargs):
        self.attrs.update(kwargs)
        return self

    def get_company(self) -> Company:
        return Company(**self.attrs)

    async def build(self, db) -> Company:
        if self.attrs.get("organization_id") == EMPTY:
            from tests.helpers.builders.organization_builder import OrganizationBuilder

            org = await OrganizationBuilder().build(db)
            self.attrs["organization_id"] = org.id

        if self.attrs.get("city_id") == EMPTY:
            from tests.helpers.builders.city_builder import CityBuilder

            city = await CityBuilder().build(db)
            self.attrs["city_id"] = city.id

        comp = Company(**self.attrs)
        db.add(comp)
        await db.flush()
        await db.refresh(comp)
        return comp
