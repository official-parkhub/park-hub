from fastapi import APIRouter

from src.modules.shared.schemas.user import LoginResponseSchema, UserCreateSchema
from src.modules.shared.services.auth_service import AuthService

router = APIRouter(tags=["Utility"])


@router.post("/login")
async def login(
    user: UserCreateSchema,
    user_service: AuthService,
) -> LoginResponseSchema:
    """
    Log in a user.
    """
    user = await user_service.authenticate_user(user.email, user.password)
    return user
