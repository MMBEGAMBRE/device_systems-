from typing import List, Optional
from app.data import users_db

def list_users(role: Optional[str] = None, is_active: Optional[bool] = None) -> List[dict]:
    filtered = users_db.users_db
    if role:
        filtered = [u for u in filtered if u["role"] == role]
    if is_active is not None:
        filtered = [u for u in filtered if u["is_active"] == is_active]
    return filtered

def find_user(user_id: int) -> Optional[dict]:
    return next((u for u in users_db.users_db if u["id"] == user_id), None)

def email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    return any(u["email"] == email and u["id"] != exclude_id for u in users_db.users_db)

def create_user(data: dict) -> dict:
    data["id"] = users_db.id_counter
    users_db.users_db.append(data)
    users_db.id_counter += 1
    return data

def update_user(user_id: int, data: dict) -> Optional[dict]:
    user = find_user(user_id)
    if user:
        user.update(data)
    return user

def delete_user(user_id: int) -> bool:
    user = find_user(user_id)
    if user:
        users_db.users_db.remove(user)
        return True
    return False
