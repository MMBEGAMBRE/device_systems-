from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: UserRole = Field(..., description="Rol del usuario: admin, support o user")
    is_active: bool = Field(True, description="Estado de activación del usuario")

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
