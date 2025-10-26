from pydantic import BaseModel


class PaginationSchema(BaseModel):
    skip: int
    limit: int
    total: int
