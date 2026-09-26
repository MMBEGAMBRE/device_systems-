from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.security import get_password_hash, verify_password
from app.models.user_model import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.scalar(select(User).where(User.email == email))


def register_user(db: Session, name: str, email: str, password: str, role: str) -> User:
    user = User(
        name=name,
        email=email,
        role=role,
        is_active=True,
        hashed_password=get_password_hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
