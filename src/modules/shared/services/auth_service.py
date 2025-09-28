from datetime import timedelta

import jwt
from sqlalchemy import select

from src.core import errors
from src.core.data.password import verify_password
from src.core.utils.base_service import BaseService
from src.core.utils.date import get_utc_now
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.shared.models.user.user import User
from src.modules.shared.schemas.user import (
    LoginResponseSchema,
    TokenData,
)
from src.settings import SETTINGS

ALGORITHM = "HS256"


@dependable
class AuthService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def authenticate_user(self, email: str, password: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user or not verify_password(password, user.password_hash):
            raise errors.AuthenticationError(message="Invalid email or password")

        return LoginResponseSchema(
            token_type="bearer",
            access_token=await self.create_jwt_token(user.id),
        )

    async def create_jwt_token(self, user_id: str):
        exp_datetime = get_utc_now() + timedelta(days=1)
        exp_timestamp = int(exp_datetime.timestamp())

        to_encode = TokenData(
            user_id=str(user_id),
            exp=exp_timestamp,
        )
        return jwt.encode(
            to_encode.model_dump(),
            SETTINGS.auth_secret_key,
            algorithm=ALGORITHM,
        )

    async def verify_jwt_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, SETTINGS.auth_secret_key, algorithms=[ALGORITHM]
            )
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise errors.AuthenticationError(message="Token has expired")
        except jwt.InvalidTokenError:
            raise errors.AuthenticationError(message="Invalid token")
