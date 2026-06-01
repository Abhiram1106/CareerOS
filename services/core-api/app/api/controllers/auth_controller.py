from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from ...dependencies import (
    current_user,
    get_confirm_reset_handler,
    get_login_handler,
    get_logout_handler,
    get_register_handler,
    get_request_reset_handler,
)
from ...models.entities import User
from ...modules.auth.dto.auth_dto import LoginRequest, PasswordResetConfirm, PasswordResetRequest, RegisterRequest
from ...modules.auth.mutation.login_handler import LoginHandler
from ...modules.auth.mutation.logout_handler import LogoutHandler
from ...modules.auth.mutation.register_handler import RegisterHandler
from ...modules.auth.mutation.reset_password_handler import ConfirmPasswordResetHandler, RequestPasswordResetHandler

router = APIRouter()


@router.post("/register")
def register(payload: RegisterRequest, handler: RegisterHandler = Depends(get_register_handler)):
    return handler.execute(payload)


@router.post("/login")
def login(payload: LoginRequest, handler: LoginHandler = Depends(get_login_handler)):
    return handler.execute(payload)


@router.post("/logout")
def logout(
    user: User = Depends(current_user),
    authorization: str | None = Header(default=None),
    handler: LogoutHandler = Depends(get_logout_handler),
):
    return handler.execute(user, authorization)


@router.post("/reset-request")
def reset_request(
    payload: PasswordResetRequest,
    handler: RequestPasswordResetHandler = Depends(get_request_reset_handler),
):
    """Request a password reset. Token printed to server logs (console-mode)."""
    return handler.execute(payload.email)


@router.post("/reset-confirm")
def reset_confirm(
    payload: PasswordResetConfirm,
    handler: ConfirmPasswordResetHandler = Depends(get_confirm_reset_handler),
):
    """Confirm a password reset with the token from server logs."""
    return handler.execute(payload.token, payload.new_password)
