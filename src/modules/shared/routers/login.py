from typing import Annotated
from fastapi import APIRouter, Depends

from src.modules.shared.schemas.user import LoginResponseSchema
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
