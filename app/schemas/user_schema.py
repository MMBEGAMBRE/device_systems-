from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    """Esquema para actualización completa (PUT)"""
    pass

class UserPatch(BaseModel):
    """Esquema para actualización parcial (PATCH)"""
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
