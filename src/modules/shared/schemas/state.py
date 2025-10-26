import uuid
from pydantic import BaseModel

from src.modules.shared.enums.country import Country


class BaseStateSchema(BaseModel):
    name: str
    country: Country
    iso2_code: str


class StateWithIDSchema(BaseStateSchema):
    id: uuid.UUID


class CreateStateSchema(BaseStateSchema):
    pass


class CreateStateResponseSchema(StateWithIDSchema):
    pass
