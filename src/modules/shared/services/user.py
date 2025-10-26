from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core import errors
from src.core.data.password import get_password_hash
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.shared.models.user.user import User
from src.modules.shared.schemas.user import (
    UserCreateSchema,
)


@dependable
class UserService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def get_user_by_id(self, id: str) -> User:
        result = await self.db.execute(
            select(User)
            .where(User.id == id)
            .options(
                selectinload(User.customer),
                selectinload(User.organization),
            )
        )
        user = result.scalars().first()

        if not user:
            raise errors.ResourceNotFound(message="User not found")
        return user

    async def user_email_exists(self, email: str) -> bool:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user is not None

    async def create_user(
        self,
        user: UserCreateSchema,
    ) -> User:
        if await self.user_email_exists(user.email):
            raise errors.ResourceAlreadyExists(message="User already exists")

        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password),
        )
        self.db.add(db_user)
        await self.db.flush()
        await self.db.refresh(db_user)

        return await self.get_user_by_id(db_user.id)
