from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr

from ...common.dto.strict import StrictModel


class RegisterRequest(StrictModel):
    email: EmailStr
    password: str
    full_name: str
    role: Literal["student", "officer", "admin"] = "student"


class LoginRequest(StrictModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    email: EmailStr
    full_name: str
    role: str
