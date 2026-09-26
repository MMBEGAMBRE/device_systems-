from datetime import date, datetime, time, timezone
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User


class UserNotFoundError(LookupError):
    pass


class DeviceNotFoundError(LookupError):
    pass


class LoanNotFoundError(LookupError):
    pass


class DeviceUnavailableError(ValueError):
    pass


class LoanAlreadyReturnedError(ValueError):
    pass


def _loan_query():
    return select(Loan).join(Loan.user).join(Loan.device).options(
        joinedload(Loan.user),
        joinedload(Loan.device),
    )


def list_loans(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[Loan]:
    statement = _loan_query()
    if status is not None:
        statement = statement.where(Loan.status == status)
    if user_email is not None:
        statement = statement.where(User.email.ilike(user_email))
    if device_type is not None:
        statement = statement.where(Device.device_type == device_type)
    if user_id is not None:
        statement = statement.where(Loan.user_id == user_id)
    if device_id is not None:
        statement = statement.where(Loan.device_id == device_id)
    if from_date is not None and to_date is not None:
        statement = statement.where(
            and_(
                Loan.loan_date >= datetime.combine(from_date, time.min, tzinfo=timezone.utc),
                Loan.loan_date <= datetime.combine(to_date, time.max, tzinfo=timezone.utc),
            )
        )
    elif from_date is not None:
        statement = statement.where(
            Loan.loan_date >= datetime.combine(from_date, time.min, tzinfo=timezone.utc)
        )
    elif to_date is not None:
        statement = statement.where(
            Loan.loan_date <= datetime.combine(to_date, time.max, tzinfo=timezone.utc)
        )
    return list(db.scalars(statement.order_by(Loan.loan_date.desc())).all())


def find_loan(db: Session, loan_id: int) -> Optional[Loan]:
    statement = _loan_query().where(Loan.id == loan_id)
    return db.scalar(statement)


def list_user_loans(db: Session, user_id: int) -> list[Loan]:
    if db.get(User, user_id) is None:
        raise UserNotFoundError("Usuario no encontrado")
    statement = _loan_query().where(Loan.user_id == user_id)
    return list(db.scalars(statement.order_by(Loan.loan_date.desc())).all())


def list_device_loans(db: Session, device_id: int) -> list[Loan]:
    if db.get(Device, device_id) is None:
        raise DeviceNotFoundError("Dispositivo no encontrado")
    statement = _loan_query().where(Loan.device_id == device_id)
    return list(db.scalars(statement.order_by(Loan.loan_date.desc())).all())


def create_loan(db: Session, user_id: int, device_id: int) -> Loan:
    user = db.get(User, user_id)
    if user is None:
        raise UserNotFoundError("Usuario no encontrado")
    device = db.get(Device, device_id)
    if device is None:
        raise DeviceNotFoundError("Dispositivo no encontrado")
    if not device.is_available:
        raise DeviceUnavailableError("El dispositivo no está disponible")

    device.is_available = False
    loan = Loan(user=user, device=device, status="active")
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int) -> Loan:
    loan = find_loan(db, loan_id)
    if loan is None:
        raise LoanNotFoundError("Préstamo no encontrado")
    if loan.status == "returned":
        raise LoanAlreadyReturnedError("El préstamo ya fue devuelto")

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)
    loan.device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan