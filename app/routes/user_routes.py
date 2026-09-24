from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserRole, UserUpdate, UserPatch
from app.services import user_service
from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse], summary="Listar usuarios", response_description="Lista de usuarios registrada")
def get_users(role: Optional[UserRole] = None, is_active: Optional[bool] = None):
    """Obtiene todos los usuarios con filtros opcionales."""
    return user_service.list_users(role, is_active)

@router.get("/{user_id}", response_model=UserResponse, summary="Consultar usuario", response_description="Usuario encontrado")
def get_user(user: dict = Depends(get_user_or_404)):
    """Busca un usuario por ID usando una dependencia inyectada."""
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar usuario", response_description="Usuario creado correctamente")
def create_user(user_in: UserCreate):
    """Registra un nuevo usuario validando correos duplicados."""
    if user_service.email_exists(user_in.email):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    return user_service.create_user(user_in.model_dump())

@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar completo", response_description="Usuario reemplazado correctamente")
def update_user(user_in: UserUpdate, existing_user: dict = Depends(get_user_or_404)):
    """Reemplaza toda la información de un usuario."""
    if user_service.email_exists(user_in.email, exclude_id=existing_user["id"]):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    return user_service.update_user(existing_user["id"], user_in.model_dump())

@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar parcial", response_description="Usuario actualizado parcialmente")
def patch_user(user_in: UserPatch, existing_user: dict = Depends(get_user_or_404)):
    """Actualiza solo los campos enviados en la petición."""
    data = user_in.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

    if "email" in data and user_service.email_exists(data["email"], exclude_id=existing_user["id"]):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    return user_service.update_user(existing_user["id"], data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario", response_description="Usuario eliminado correctamente")
def delete_user(existing_user: dict = Depends(get_user_or_404)):
    """Elimina definitivamente un usuario."""
    user_service.delete_user(existing_user["id"])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
