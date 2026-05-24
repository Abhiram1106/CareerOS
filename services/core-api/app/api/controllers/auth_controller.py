from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from ...dependencies import current_user, get_login_handler, get_logout_handler, get_register_handler
from ...models.entities import User
from ...modules.auth.dto.auth_dto import LoginRequest, RegisterRequest
from ...modules.auth.mutation.login_handler import LoginHandler
from ...modules.auth.mutation.logout_handler import LogoutHandler
from ...modules.auth.mutation.register_handler import RegisterHandler

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
