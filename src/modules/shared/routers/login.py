from typing import Annotated
from fastapi import APIRouter, Depends, Response, Cookie

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
    response: Response,
) -> LoginResponseSchema:
    """
    Log in a user.
    """
    userWithRefresh = await user_service.authenticate_user(
        form_data.username, form_data.password
    )
    response.set_cookie(
        key="refresh_token",
        value=userWithRefresh.refresh_token,
        httponly=True,
        samesite="lax",
    )
    return LoginResponseSchema(
        token_type=userWithRefresh.token_type,
        access_token=userWithRefresh.access_token,
    )


@router.get("/me")
async def get_current_user(
    current_user: DepCurrentUser,
) -> UserWithoutPasswordSchema:
    """
    Get the currently authenticated user.
    """
    return current_user


@router.post("/refresh")
async def refresh_token(
    refresh_token: Annotated[str | None, Cookie()],
    user_service: AuthService,
) -> LoginResponseSchema:
    """
    Refresh the JWT token using the refresh token from the cookie.
    """
    response = await user_service.authenticate_refresh_token(refresh_token)
    return response
