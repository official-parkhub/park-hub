from typing import Annotated
from fastapi import APIRouter, Depends

from src.modules.shared.dependencies.auth import DepCurrentUser
from src.modules.shared.schemas.user import (
    LoginResponseSchema,
    UserWithoutPasswordSchema,
)
from src.modules.shared.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Utility"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: AuthService,
) -> LoginResponseSchema:
    """
    Log in a user.
    """
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    return user


@router.get("/me")
async def get_current_user(
    current_user: DepCurrentUser,
) -> UserWithoutPasswordSchema:
    """
    Get the currently authenticated user.
    """
    return current_user
