from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...modules.auth.dto.auth_dto import LoginRequest, RegisterRequest
from ...modules.auth.mutation.login_handler import LoginHandler
from ...modules.auth.mutation.register_handler import RegisterHandler

router = APIRouter()


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return RegisterHandler(db).execute(payload)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return LoginHandler(db).execute(payload)
