from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.auth.security import create_access_token, limiter
from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import Token, UserRegister
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un usuario nuevo validando contraseña segura y correo único.",
    response_description="Usuario registrado sin exponer la contraseña",
)
@limiter.limit("3/minute")
def register(request: Request, payload: UserRegister, db: Session = Depends(get_db)):
    if auth_service.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    return auth_service.register_user(db, payload.name, payload.email, payload.password, payload.role.value)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica al usuario y retorna un token de acceso JWT.",
    response_description="Token de acceso Bearer",
)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Usuario autenticado",
    description="Retorna los datos del usuario dueño del token enviado.",
    response_description="Datos del usuario actual",
)
def me(current_user=Depends(get_current_active_user)):
    return current_user
