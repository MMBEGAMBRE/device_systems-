from typing import Literal, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import User


def list_users(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    sort_by: Literal["name", "created_at"] = "name",
) -> list[User]:
    statement = select(User)
    if role is not None:
        statement = statement.where(User.role == role)
    if is_active is not None:
        statement = statement.where(User.is_active == is_active)
    sort_column = User.name if sort_by == "name" else User.created_at
    return list(db.scalars(statement.order_by(sort_column)).all())


def find_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def find_user_by_email(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def create_user(db: Session, data: dict) -> User:
    user = User(**data)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("El correo electrónico ya está registrado") from exc
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: dict) -> User:
    for field, value in data.items():
        setattr(user, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("El correo electrónico ya está registrado") from exc
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("No se puede eliminar el usuario porque tiene préstamos registrados") from exc
