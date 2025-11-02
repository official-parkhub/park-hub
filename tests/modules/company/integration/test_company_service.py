import pytest

from src.modules.company.services.company import CompanyService
from src.modules.company.schemas.company.create_company import CreateCompanySchema
from tests.helpers.builders.city_builder import CityBuilder
from tests.helpers.builders.organization_builder import OrganizationBuilder
from tests.helpers.db_utils import clear_database


class _StubCompanyPriceService:
    async def get_parking_price_reference(self, company_id: str):
        return None


class TestCompanyService:
    @pytest.fixture(autouse=True)
    async def setup(self, rc, db):
        self.service = CompanyService(rc)
        await clear_database(db)

    async def test_create_and_get_company(self, db, faker):
        org = await OrganizationBuilder().build(db)
        city = await CityBuilder().build(db)

        payload = CreateCompanySchema(
            city_id=city.id,
            name=faker.company(),
            postal_code=faker.postcode(),
            register_code=faker.unique.ean(length=13),
            address=faker.street_address(),
            description=faker.sentence(),
            is_covered=faker.boolean(),
            has_camera=faker.boolean(),
            total_spots=faker.random_int(min=5, max=50),
            has_charging_station=faker.boolean(),
        )

        company = await self.service.create_company(str(org.id), payload)
        assert company.id
        fetched = await self.service.get_company_by_id(str(company.id))
        assert fetched.id == company.id

    async def test_create_company_duplicate_register_code(self, db, faker):
        org = await OrganizationBuilder().build(db)
        city = await CityBuilder().build(db)

        reg = faker.unique.ean(length=13)
        payload = CreateCompanySchema(
            city_id=city.id,
            name=faker.company(),
            postal_code=faker.postcode(),
            register_code=reg,
            address=faker.street_address(),
            description=None,
            is_covered=False,
            has_camera=False,
            total_spots=10,
            has_charging_station=False,
        )
        await self.service.create_company(str(org.id), payload)

        with pytest.raises(Exception):
            await self.service.create_company(str(org.id), payload)

    async def test_list_companies_basic(self, db, faker):
        # create a couple of companies
        for _ in range(2):
            org = await OrganizationBuilder().build(db)
            city = await CityBuilder().build(db)
            payload = CreateCompanySchema(
                city_id=city.id,
                name=faker.company(),
                postal_code=faker.postcode(),
                register_code=faker.unique.ean(length=13),
                address=faker.street_address(),
                description=None,
                is_covered=False,
                has_camera=False,
                total_spots=10,
                has_charging_station=False,
            )
            await self.service.create_company(str(org.id), payload)

        result = await self.service.list_companies(
            skip=0, limit=10, company_price_service=_StubCompanyPriceService()
        )
        assert result.total >= 2
        assert len(result.data) >= 2
