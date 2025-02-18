from typing import List, Annotated, Optional

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies.auth import get_current_user, get_current_owner, get_current_admin
from app.schemas.admin import AdminOut
from app.schemas.owner import OwnerOut
from app.schemas.token import Token
from app.schemas.user import UserOut, UserUpdate, UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=UserOut)
async def get_user_profile(
        current_user: Annotated[UserOut, Depends(get_current_user)],
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return current_user


@router.get("/", response_model=List[UserOut])
def get_all_users(
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    service = UserService(db)

    if current_owner:
        return service.get_all()

    if current_admin:
        return service.get_all_users_for_admin(current_admin)

    if current_user:
        return service.get_all_users_for_user(current_user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    service = UserService(db)

    if current_owner:
        return service.get_by_id(user_id)

    if current_admin:
        return service.get_user_by_id_for_admin(user_id, current_admin)

    if current_user:
        return service.get_user_by_id_for_user(user_id, current_user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=UserOut)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
):
    service = UserService(db)

    if current_owner:
        return service.create(user)

    if current_admin:
        return service.create_by_admin(user, current_admin)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{user_id}", response_model=UserOut)
def update_user(
        user_id: int,
        user: UserUpdate,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
):
    service = UserService(db)

    if current_owner:
        return service.update(user_id, user)

    if current_admin:
        return service.update_by_admin(user_id, user, current_admin)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{user_id}", response_model=UserOut)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
):
    service = UserService(db)

    if current_owner:
        return service.delete(user_id)

    if current_admin:
        return service.delete_by_admin(user_id, current_admin)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/login", response_model=Token)
def login_for_user_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate_user(form_data.username, form_data.password)
    access_token = UserService.create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
