import uuid

from src.modules.company.schemas.company.company import BaseCompanySchema


class CreateCompanySchema(BaseCompanySchema):
    city_id: uuid.UUID
