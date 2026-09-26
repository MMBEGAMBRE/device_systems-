from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_admin, require_staff
from app.dependencies.database_dependency import get_db
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceResponse, DeviceType, DeviceUpdate
from app.schemas.loan_schema import LoanDetailResponse
from app.services import device_service, loan_service

router = APIRouter(prefix="/devices", tags=["Devices"])


def get_device_or_404(device_id: int, db: Session = Depends(get_db)) -> Device:
    device = device_service.find_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar y filtrar dispositivos",
    description="Filtra por tipo, disponibilidad, marca o texto en nombre/serie.",
    response_description="Dispositivos que coinciden con los filtros",
)
def get_devices(
    device_type: Optional[DeviceType] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Literal["name", "created_at"] = "name",
    db: Session = Depends(get_db),
):
    return device_service.list_devices(db, device_type, is_available, brand, search, sort_by)


@router.get(
    "/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar historial del dispositivo",
    response_description="Préstamos históricos del dispositivo con datos relacionados",
)
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    try:
        return loan_service.list_device_loans(db, device_id)
    except loan_service.DeviceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo",
    response_description="Dispositivo encontrado",
)
def get_device(device: Device = Depends(get_device_or_404)):
    return device


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar dispositivo",
    response_description="Dispositivo creado correctamente",
)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db), current_user=Depends(require_staff)):
    if device_service.find_device_by_serial(db, device_in.serial_number):
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    try:
        return device_service.create_device(db, device_in.model_dump(mode="json"))
    except device_service.DuplicateSerialError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    response_description="Dispositivo reemplazado correctamente",
)
def update_device(
    device_in: DeviceUpdate,
    device: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
    current_user=Depends(require_staff),
):
    duplicate = device_service.find_device_by_serial(db, device_in.serial_number)
    if duplicate and duplicate.id != device.id:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    try:
        return device_service.update_device(db, device, device_in.model_dump(mode="json"))
    except device_service.DeviceHasActiveLoanError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except device_service.DuplicateSerialError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente",
    response_description="Dispositivo actualizado parcialmente",
)
def patch_device(
    device_in: DevicePatch,
    device: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
):
    data = device_in.model_dump(exclude_unset=True, exclude_none=True, mode="json")
    if not data:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")
    if "serial_number" in data:
        duplicate = device_service.find_device_by_serial(db, data["serial_number"])
        if duplicate and duplicate.id != device.id:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    try:
        return device_service.update_device(db, device, data)
    except device_service.DeviceHasActiveLoanError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except device_service.DuplicateSerialError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    response_description="Dispositivo eliminado correctamente",
)
def delete_device(
    device: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        device_service.delete_device(db, device)
    except device_service.DeviceHasLoansError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)