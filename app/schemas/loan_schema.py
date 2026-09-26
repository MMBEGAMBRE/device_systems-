from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class LoanStatus(str, Enum):
    active = "active"
    returned = "returned"
    overdue = "overdue"


class LoanCreate(BaseModel):
    user_id: int = Field(gt=0)
    device_id: int = Field(gt=0)

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"user_id": 1, "device_id": 1}]}
    )


class LoanUpdate(BaseModel):
    status: LoanStatus


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: LoanStatus

    model_config = ConfigDict(from_attributes=True)


class LoanUserSummary(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LoanDeviceSummary(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(LoanResponse):
    user: LoanUserSummary
    device: LoanDeviceSummary

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "device_id": 1,
                    "loan_date": "2026-09-25T12:00:00Z",
                    "return_date": None,
                    "status": "active",
                    "user": {"id": 1, "name": "Ana Perez", "email": "ana@example.com"},
                    "device": {
                        "id": 1,
                        "name": "Laptop ThinkPad",
                        "serial_number": "LEN-2026-001",
                        "device_type": "laptop",
                    },
                }
            ]
        }
    )