from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.admin_repo import AdminRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.admin_service import AdminService
from app.services.user_service import UserService


oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
oauth2_admin_scheme = OAuth2PasswordBearer(tokenUrl="admins/login")

auth_service = AuthService()

def get_current_user(token: str = Depends(oauth2_user_scheme), db: Session = Depends(get_db)):
    try:
        payload = auth_service.verify_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user_repo = UserRepository(db)
        user = user_repo.get_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def get_current_admin(token: str = Depends(oauth2_admin_scheme), db: Session = Depends(get_db)):
    try:
        payload = auth_service.verify_token(token)
        username: str = payload.get("sub")

        if username is None or payload.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        admin_repo = AdminRepository(db)
        admin = admin_repo.get_by_username(username)

        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return admin

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
