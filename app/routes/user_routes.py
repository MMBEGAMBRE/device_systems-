from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserRole

router = APIRouter(prefix="/users", tags=["Users"])

# Almacenamiento en memoria
users_db = []
id_counter = 1

@router.get("/", response_model=List[UserResponse], summary="Listar todos los usuarios")
def get_users(
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None
):
    """
    Lista todos los usuarios con filtros opcionales por rol y estado activo.
    """
    filtered_users = users_db
    if role:
        filtered_users = [u for u in filtered_users if u["role"] == role]
    if is_active is not None:
        filtered_users = [u for u in filtered_users if u["is_active"] == is_active]
    return filtered_users

@router.get("/{user_id}", response_model=UserResponse, summary="Consultar usuario por ID")
def get_user(user_id: int):
    """
    Busca un usuario específico por su ID único.
    """
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
def create_user(user_in: UserCreate):
    """
    Registra un nuevo usuario validando que el correo no esté duplicado.
    """
    global id_counter

    # Validar correos duplicados
    if any(u["email"] == user_in.email for u in users_db):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    new_user = user_in.model_dump()
    new_user["id"] = id_counter
    users_db.append(new_user)
    id_counter += 1
    return new_user
