from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status as http_status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.auth.security import limiter
from app.dependencies.auth_dependency import get_current_active_user, require_staff
from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceType
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanStatus
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])


def _raise_loan_error(exc: Exception) -> None:
    if isinstance(exc, (loan_service.UserNotFoundError, loan_service.DeviceNotFoundError,
                        loan_service.LoanNotFoundError)):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, (loan_service.DeviceUnavailableError,
                        loan_service.LoanAlreadyReturnedError)):
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    raise exc


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos con usuario y dispositivo",
    description="Une loans con users y devices, y permite filtrar por estado, email, tipo y fechas.",
    response_description="Préstamos con información relacionada",
)
def get_loan_details(
    status: Optional[LoanStatus] = None,
    user_email: Optional[EmailStr] = None,
    device_type: Optional[DeviceType] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_staff),
):
    if from_date and to_date and from_date > to_date:
        raise HTTPException(status_code=422, detail="from_date debe ser anterior o igual a to_date")
    return loan_service.list_loans(
        db,
        status=status.value if status else None,
        user_email=str(user_email) if user_email else None,
        device_type=device_type.value if device_type else None,
        from_date=from_date,
        to_date=to_date,
    )


@router.get(
    "",
    response_model=list[LoanDetailResponse],
    summary="Listar y filtrar préstamos",
    description="Filtra el historial por estado, usuario, email, dispositivo, tipo y rango de fechas.",
    response_description="Préstamos con datos de usuario y dispositivo",
)
def get_loans(
    status: Optional[LoanStatus] = None,
    user_email: Optional[EmailStr] = None,
    device_type: Optional[DeviceType] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    if from_date and to_date and from_date > to_date:
        raise HTTPException(status_code=422, detail="from_date debe ser anterior o igual a to_date")
    return loan_service.list_loans(
        db,
        status=status.value if status else None,
        user_email=str(user_email) if user_email else None,
        device_type=device_type.value if device_type else None,
        user_id=user_id,
        device_id=device_id,
        from_date=from_date,
        to_date=to_date,
    )


@router.post(
    "",
    response_model=LoanDetailResponse,
    status_code=http_status.HTTP_201_CREATED,
    summary="Prestar dispositivo",
    description="Valida usuario y disponibilidad, crea el préstamo y marca el dispositivo como no disponible.",
    response_description="Préstamo registrado con usuario y dispositivo",
)
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    loan_in: LoanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    try:
        return loan_service.create_loan(db, loan_in.user_id, loan_in.device_id)
    except (loan_service.UserNotFoundError, loan_service.DeviceNotFoundError,
            loan_service.DeviceUnavailableError) as exc:
        _raise_loan_error(exc)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanDetailResponse,
    summary="Devolver dispositivo",
    description="Marca el préstamo como devuelto y restablece la disponibilidad del dispositivo.",
    response_description="Préstamo devuelto",
)
def return_loan(loan_id: int, db: Session = Depends(get_db), current_user=Depends(require_staff)):
    try:
        return loan_service.return_loan(db, loan_id)
    except (loan_service.LoanNotFoundError, loan_service.LoanAlreadyReturnedError) as exc:
        _raise_loan_error(exc)


@router.get(
    "/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Consultar préstamo",
    response_description="Préstamo con usuario y dispositivo",
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.find_loan(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan