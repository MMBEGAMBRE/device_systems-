from fastapi import HTTPException, status
from app.services import user_service

def get_user_or_404(user_id: int) -> dict:
    user = user_service.find_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user
