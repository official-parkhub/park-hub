from typing import Annotated

from src.modules.shared.models.user.user import User
from src.modules.shared.services.auth_service import AuthService

from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends
from src.core import errors
from src.modules.shared.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/core/login",
    auto_error=False,
)


async def _get_current_user_token(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    auth_service: AuthService,
    user_service: UserService,
) -> User:
    if not token:
        raise errors.AuthenticationError(message="Not authenticated")

    user_data = await auth_service.verify_jwt_token(token)
    user = await user_service.get_user_by_id(user_data.user_id)

    return user


DepCurrentUser = Annotated[
    User,
    Depends(_get_current_user_token),
]
