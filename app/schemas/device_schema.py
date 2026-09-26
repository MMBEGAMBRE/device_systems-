from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class DeviceType(str, Enum):
    laptop = "laptop"
    tablet = "tablet"
    projector = "proyector"
    camera = "camara"
    router = "router"
    monitor = "monitor"


class DeviceCreate(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    serial_number: str = Field(min_length=2, max_length=100)
    device_type: DeviceType
    brand: str | None = Field(default=None, max_length=80)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Laptop ThinkPad",
                    "serial_number": "LEN-2026-001",
                    "device_type": "laptop",
                    "brand": "Lenovo",
                }
            ]
        }
    )


class DeviceUpdate(DeviceCreate):
    is_available: bool


class DevicePatch(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=150)
    serial_number: str | None = Field(default=None, min_length=2, max_length=100)
    device_type: DeviceType | None = None
    brand: str | None = Field(default=None, max_length=80)
    is_available: bool | None = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: DeviceType
    brand: str | None
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)