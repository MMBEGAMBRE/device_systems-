from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserResponse, UserRole, UserUpdate, UserPatch
from app.services import user_service
from app.dependencies.database_dependency import get_db
from app.dependencies.user_dependencies import get_user_or_404
from app.schemas.loan_schema import LoanDetailResponse
from app.services import loan_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserResponse], summary="Listar usuarios", response_description="Lista de usuarios registrada")
def get_users(
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    sort_by: Literal["name", "created_at"] = "name",
    db: Session = Depends(get_db),
):
    """Obtiene todos los usuarios con filtros opcionales."""
    return user_service.list_users(db, role, is_active, sort_by)

@router.get("/{user_id}", response_model=UserResponse, summary="Consultar usuario", response_description="Usuario encontrado")
def get_user(user=Depends(get_user_or_404)):
    """Busca un usuario por ID usando una dependencia inyectada."""
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar usuario", response_description="Usuario creado correctamente")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario validando correos duplicados."""
    if user_service.find_user_by_email(db, str(user_in.email)):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    try:
        return user_service.create_user(db, user_in.model_dump(mode="json"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar completo", response_description="Usuario reemplazado correctamente")
def update_user(
    user_in: UserUpdate,
    existing_user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    """Reemplaza toda la información de un usuario."""
    duplicate = user_service.find_user_by_email(db, str(user_in.email))
    if duplicate and duplicate.id != existing_user.id:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    try:
        return user_service.update_user(db, existing_user, user_in.model_dump(mode="json"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar parcial", response_description="Usuario actualizado parcialmente")
def patch_user(
    user_in: UserPatch,
    existing_user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    """Actualiza solo los campos enviados en la petición."""
    data = user_in.model_dump(exclude_unset=True, exclude_none=True, mode="json")
    if not data:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

    if "email" in data:
        duplicate = user_service.find_user_by_email(db, data["email"])
        if duplicate and duplicate.id != existing_user.id:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    try:
        return user_service.update_user(db, existing_user, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario", response_description="Usuario eliminado correctamente")
def delete_user(existing_user=Depends(get_user_or_404), db: Session = Depends(get_db)):
    """Elimina definitivamente un usuario."""
    try:
        user_service.delete_user(db, existing_user)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos del usuario",
    response_description="Historial de préstamos con información de los dispositivos",
)
def get_user_loans(
    existing_user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    return loan_service.list_user_loans(db, existing_user.id)
