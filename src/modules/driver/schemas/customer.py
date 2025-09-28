from pydantic import BaseModel, Field
from datetime import date
import uuid


class CustomerCreateSchema(BaseModel):
    first_name: str = Field(
        ..., min_length=1, max_length=50, description="Customer's first name"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=50, description="Customer's last name"
    )
    birth_date: date = Field(
        ..., description="Customer's birth date in YYYY-MM-DD format"
    )


class CustomerResponseSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    first_name: str
    last_name: str
    birth_date: date

    class Config:
        from_attributes = True
