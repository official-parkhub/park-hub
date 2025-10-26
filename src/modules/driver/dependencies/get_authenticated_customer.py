from typing import Annotated
from src.core.errors import errors
from src.modules.driver.models.customer import Customer
from src.modules.shared.dependencies.auth import DepCurrentUser


async def _get_authenticated_customer(
    User: DepCurrentUser,
) -> Customer:
    if not User.customer:
        raise errors.ResourceNotFound(message="Authenticated customer not found")

    return User.customer


DepAuthenticatedCustomer = Annotated[
    Customer,
    _get_authenticated_customer,
]
