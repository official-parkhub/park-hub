import pytest
from tests.helpers.builders.organization_builder import OrganizationBuilder
from tests.helpers.builders.city_builder import CityBuilder
from tests.helpers.builders.user_builder import UserBuilder
from tests.helpers.db_utils import clear_database
from tests.helpers.mocks.auth import mock_get_current_user
from uuid import uuid4


class TestCompanyRoute:
    @pytest.fixture(autouse=True)
    async def setup(self, db):
        await clear_database(db)

    async def test_create_and_get_company(self, client, db, faker):
        user = await UserBuilder().customize(is_admin=True).build(db)
        org = await OrganizationBuilder().customize(user_id=user.id).build(db)
        user.organization = org
        city = await CityBuilder().build(db)

        patch = mock_get_current_user(client, user)

        payload = {
            "city_id": str(city.id),
            "name": faker.company(),
            "postal_code": faker.postcode(),
            "register_code": str(uuid4()),
            "address": faker.street_address(),
            "description": faker.sentence(),
            "is_covered": faker.boolean(),
            "has_camera": faker.boolean(),
            "total_spots": faker.random_int(min=5, max=50),
            "has_charging_station": faker.boolean(),
        }
        resp = client.post("/api/core/company/", json=payload)
        assert resp.status_code == 201
        company = resp.json()
        company_id = company["id"]

        get_resp = client.get(f"/api/core/company/{company_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == company_id
        patch.stop()
