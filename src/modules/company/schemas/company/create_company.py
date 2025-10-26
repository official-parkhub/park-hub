import uuid
from pydantic import BaseModel

from src.modules.company.schemas.company.company import BaseCompanySchema


class CreateCompanySchema(BaseModel, BaseCompanySchema):
    city_id: uuid.UUID
