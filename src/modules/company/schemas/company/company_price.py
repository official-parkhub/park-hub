import uuid

from src.modules.company.schemas.company.company import BaseParkingPriceSchema


class CreateParkingPriceSchema(BaseParkingPriceSchema):
    company_id: uuid.UUID
    pass


class CreateParkingPriceResponseSchema(BaseParkingPriceSchema):
    id: uuid.UUID
