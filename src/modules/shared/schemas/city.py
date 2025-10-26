import uuid
from pydantic import BaseModel

from src.modules.shared.enums.country import Country
from src.modules.shared.schemas.state import BaseStateSchema


class BaseCitySchema(BaseModel):
    name: str
    identification_code: str | None = None
    country: Country


class CityWithIDSchema(BaseCitySchema):
    id: uuid.UUID
    state: BaseStateSchema | None = None


class CreateCitySchema(BaseCitySchema):
    state_id: uuid.UUID | None = None


class CreateCityResponseSchema(CityWithIDSchema):
    pass
