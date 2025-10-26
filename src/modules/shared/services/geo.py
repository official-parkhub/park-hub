from sqlalchemy import select

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.shared.models.geo.state import State
from src.modules.shared.models.geo.city import City
from src.modules.shared.schemas.state import CreateStateSchema, StateWithIDSchema
from src.modules.shared.schemas.city import CreateCitySchema, CityWithIDSchema


@dependable
class GeoService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def create_state(
        self,
        state: CreateStateSchema,
    ) -> StateWithIDSchema:
        db_state = State(
            name=state.name,
            country=state.country,
            iso2_code=state.iso2_code,
        )
        self.db.add(db_state)
        await self.db.flush()
        await self.db.refresh(db_state)

        return StateWithIDSchema(
            id=db_state.id,
            name=db_state.name,
            country=db_state.country,
            iso2_code=db_state.iso2_code,
        )

    async def get_state_by_id(
        self,
        state_id: str,
    ) -> State | None:
        result = await self.db.execute(select(State).where(State.id == state_id))
        return result.scalars().first()

    async def create_city(
        self,
        city: CreateCitySchema,
    ) -> CityWithIDSchema:
        if city.state_id:
            state = await self.get_state_by_id(city.state_id)
            if not state:
                raise errors.ResourceNotFound(message="State not found")

        db_city = City(
            name=city.name,
            identification_code=city.identification_code,
            country=city.country,
            state_id=city.state_id,
        )
        self.db.add(db_city)
        await self.db.flush()
        await self.db.refresh(db_city)

        return CityWithIDSchema(
            id=db_city.id,
            name=db_city.name,
            identification_code=db_city.identification_code,
            country=db_city.country,
            state=(
                None
                if getattr(db_city, "state", None) is None
                else {
                    "name": db_city.state.name,
                    "country": db_city.state.country,
                    "iso2_code": getattr(db_city.state, "iso2_code", None),
                }
            ),
        )
