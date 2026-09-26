import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user_schema import UserRole


class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    role: UserRole = UserRole.user

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Ana Perez",
                    "email": "ana@example.com",
                    "password": "Segura123",
                    "role": "user",
                }
            ]
        }
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if " " in value:
            raise ValueError("La contraseña no debe contener espacios en blanco")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe tener al menos un número")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
