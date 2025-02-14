from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.user import UserOut, UserBase
from app.schemas.token import Token
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all()


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_by_id(user_id)


@router.post("/", response_model=UserOut)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update(user_id, user)


@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete(user_id)


@router.post("/login", response_model=Token)
def login_for_user_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate_user(form_data.username, form_data.password)
    access_token = UserService.create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}