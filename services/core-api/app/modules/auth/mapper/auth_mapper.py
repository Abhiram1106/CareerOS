from __future__ import annotations

from ..dto.auth_dto import AuthResponse
from ....models.entities import User


def to_auth_response(user: User, token: str) -> AuthResponse:
    return AuthResponse(
        token=token,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
    )
