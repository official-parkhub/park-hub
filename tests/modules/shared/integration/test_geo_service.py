import pytest

from src.modules.shared.services.geo import GeoService
from src.modules.shared.schemas.state import CreateStateSchema
from src.modules.shared.schemas.city import CreateCitySchema
from src.modules.shared.enums.country import Country
from tests.helpers.db_utils import clear_database


class TestGeoService:
    @pytest.fixture(autouse=True)
    async def setup(self, rc, db):
        self.service = GeoService(rc)
        await clear_database(db)

    async def test_create_state_and_city_with_state(self, faker):
        st = await self.service.create_state(
            CreateStateSchema(
                name=faker.state(),
                country=Country.BR,
                iso2_code=faker.bothify("??").upper(),
            )
        )
        assert st.id
        city = await self.service.create_city(
            CreateCitySchema(
                name=faker.city(),
                identification_code=faker.postcode(),
                country=Country.BR,
                state_id=st.id,
            )
        )
        assert city.id
        assert city.state is not None
        assert city.state.iso2_code

    async def test_create_city_missing_state_raises(self, faker):
        with pytest.raises(Exception):
            await self.service.create_city(
                CreateCitySchema(
                    name=faker.city(),
                    identification_code=faker.postcode(),
                    country=Country.BR,
                    state_id=faker.uuid4(),
                )
            )
