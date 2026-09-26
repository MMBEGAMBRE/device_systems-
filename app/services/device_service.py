from typing import Literal, Optional

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan


class DuplicateSerialError(ValueError):
    pass


class DeviceHasLoansError(ValueError):
    pass


class DeviceHasActiveLoanError(ValueError):
    pass


def list_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Literal["name", "created_at"] = "name",
) -> list[Device]:
    statement = select(Device)
    if device_type is not None:
        statement = statement.where(Device.device_type == device_type)
    if is_available is not None:
        statement = statement.where(Device.is_available == is_available)
    if brand:
        statement = statement.where(Device.brand.ilike(f"%{brand}%"))
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Device.name.ilike(pattern),
                Device.serial_number.ilike(pattern),
                Device.brand.ilike(pattern),
            )
        )
    sort_column = Device.name if sort_by == "name" else Device.created_at
    return list(db.scalars(statement.order_by(sort_column)).all())


def find_device(db: Session, device_id: int) -> Optional[Device]:
    return db.get(Device, device_id)


def find_device_by_serial(db: Session, serial_number: str) -> Optional[Device]:
    return db.scalar(select(Device).where(Device.serial_number == serial_number))


def create_device(db: Session, data: dict) -> Device:
    device = Device(**data)
    db.add(device)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateSerialError("El número de serie ya está registrado") from exc
    db.refresh(device)
    return device


def update_device(db: Session, device: Device, data: dict) -> Device:
    if data.get("is_available") is True and not device.is_available:
        active_loan_id = db.scalar(
            select(Loan.id).where(Loan.device_id == device.id, Loan.status == "active")
        )
        if active_loan_id is not None:
            raise DeviceHasActiveLoanError(
                "No se puede marcar disponible un dispositivo con un préstamo activo"
            )
    for field, value in data.items():
        setattr(device, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateSerialError("El número de serie ya está registrado") from exc
    db.refresh(device)
    return device


def delete_device(db: Session, device: Device) -> None:
    db.delete(device)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DeviceHasLoansError(
            "No se puede eliminar el dispositivo porque tiene préstamos registrados"
        ) from exc