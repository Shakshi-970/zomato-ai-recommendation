from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .service import register, login, get_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    name: str
    email: str
    token: str


@router.post("/register", response_model=UserResponse)
def register_user(request: RegisterRequest) -> UserResponse:
    try:
        result = register(request.name, request.email, request.password)
        return UserResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Register error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed.")


@router.post("/login", response_model=UserResponse)
def login_user(request: LoginRequest) -> UserResponse:
    try:
        result = login(request.email, request.password)
        return UserResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed.")


@router.get("/me")
def get_me(token: str) -> dict:
    user = get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session.")
    return user
