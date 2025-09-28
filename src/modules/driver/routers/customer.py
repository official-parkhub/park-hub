from fastapi import APIRouter

from src.modules.driver.schemas.customer import (
    CustomerCreateSchema,
    CustomerResponseSchema,
)
from src.modules.driver.services.customer import CustomerService
from src.modules.shared.schemas.user import UserCreateSchema
from src.modules.shared.services.user import UserService

router = APIRouter(tags=["Customer"])


@router.post("/customer")
async def create_customer(
    customer: CustomerCreateSchema,
    user: UserCreateSchema,
    user_service: UserService,
    customer_service: CustomerService,
) -> CustomerResponseSchema:
    """
    Create a new customer.
    """
    user = await user_service.create_user(user)
    result = await customer_service.create_customer(user.id, customer)
    return result
