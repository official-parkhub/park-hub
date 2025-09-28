from typing import Literal
from pydantic import BaseModel, EmailStr, Field


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
