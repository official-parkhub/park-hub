from typing import Literal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
import uuid

from src.modules.company.schemas.organization import OrganizationSchema
from src.modules.driver.schemas.customer import CustomerResponseSchema


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginResponseSchema(BaseModel):
    token_type: Literal["bearer"]
    access_token: str


class TokenData(BaseModel):
    user_id: str
    exp: int


class UserWithoutPasswordSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_admin: bool
    customer: Optional[CustomerResponseSchema] = None
    organization: Optional[OrganizationSchema] = None

    model_config = ConfigDict(from_attributes=True)
