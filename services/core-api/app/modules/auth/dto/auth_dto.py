from __future__ import annotations

from pydantic import BaseModel, EmailStr

from ...common.dto.strict import StrictModel


class RegisterRequest(StrictModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(StrictModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    email: EmailStr
    full_name: str
    role: str


class PasswordResetRequest(StrictModel):
    email: EmailStr


class PasswordResetConfirm(StrictModel):
    token: str
    new_password: str
