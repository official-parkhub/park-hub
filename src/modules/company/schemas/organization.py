from pydantic import BaseModel, Field, ConfigDict
import uuid

from src.modules.shared.schemas.state import StateWithIDSchema


class OrganizationCreateSchema(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Organization's name"
    )
    register_code: str = Field(
        ..., min_length=1, max_length=50, description="Organization's register code"
    )
    state_id: uuid.UUID = Field(..., description="Organization's state UUID")


class OrganizationResponseSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    register_code: str
    state_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class OrganizationSchema(OrganizationResponseSchema):
    state: StateWithIDSchema
