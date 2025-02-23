from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.admin_repo import AdminRepository
from app.repositories.owner_repo import OwnerRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService


oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="users/login", auto_error=False)
oauth2_admin_scheme = OAuth2PasswordBearer(tokenUrl="admins/login", auto_error=False)
oauth2_owner_scheme = OAuth2PasswordBearer(tokenUrl="owner/login", auto_error=False)

auth_service = AuthService()


def get_current_user(token: Optional[str] = Depends(oauth2_user_scheme), db: Session = Depends(get_db)):
    if not token:
        return None

    payload = auth_service.verify_token(token)
    if payload.get("role") != "user":
        return None

    user_repo = UserRepository(db)
    return user_repo.get_by_username(payload.get("sub"))


def get_current_admin(token: Optional[str] = Depends(oauth2_admin_scheme), db: Session = Depends(get_db)):
    if not token:
        return None

    payload = auth_service.verify_token(token)
    if payload.get("role") != "admin":
        return None

    admin_repo = AdminRepository(db)
    return admin_repo.get_by_username(payload.get("sub"))


def get_current_owner(token: Optional[str] = Depends(oauth2_owner_scheme), db: Session = Depends(get_db)):
    if not token:
        return None

    payload = auth_service.verify_token(token)
    if payload.get("role") != "owner":
        return None

    owner_repo = OwnerRepository(db)
    return owner_repo.get_by_username(payload.get("sub"))
