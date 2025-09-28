from sqlalchemy import select

from src.core import errors
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.driver.models.customer import Customer
from src.modules.driver.schemas.customer import CustomerCreateSchema


@dependable
class CustomerService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def get_customer_by_id(self, id: str):
        result = await self.db.execute(select(Customer).where(Customer.id == id))
        customer = result.scalars().first()
        if not customer:
            raise errors.ResourceNotFound(message="Customer not found")
        return customer

    async def create_customer(
        self,
        user_id: str,
        customer: CustomerCreateSchema,
    ) -> Customer:
        db_customer = Customer(
            user_id=user_id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            birth_date=customer.birth_date,
        )
        self.db.add(db_customer)
        await self.db.flush()
        await self.db.refresh(db_customer)

        return await self.get_customer_by_id(db_customer.id)
