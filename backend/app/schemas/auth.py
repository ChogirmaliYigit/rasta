from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from app.schemas.common import UserRole
import uuid

class LoginRequest(BaseModel):
    phone: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    model_config = ConfigDict(from_attributes=True)

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    model_config = ConfigDict(from_attributes=True)
