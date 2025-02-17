from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependecies.auth import get_current_admin, get_current_owner, get_current_user
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from app.schemas.owner import OwnerOut
from app.schemas.token import Token
from app.schemas.user import UserOut
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/profile", response_model=AdminOut)
async def get_admin_profile(
        current_admin: Annotated[AdminOut, Depends(get_current_admin)],
):
    if current_admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return current_admin


@router.get("/", response_model=List[AdminOut])
def get_all_admins(
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    service = AdminService(db)

    if current_owner:
        return service.get_all()

    if current_admin:
        return service.get_all_admins_for_admin(current_admin)

    if current_user:
        return service.get_all_admins_for_user(current_user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{admin_id}", response_model=AdminOut)
def get_admin_by_id(
        admin_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    service = AdminService(db)

    if current_owner:
        return service.get_by_id(admin_id)

    if current_admin:
        return service.get_admin_by_id_for_admin(admin_id, current_admin)

    if current_user:
        return service.get_admin_by_id_for_user(admin_id, current_user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=AdminOut)
def create_admin(
        admin: AdminCreate,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = AdminService(db)
        return service.create(admin)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{admin_id}", response_model=AdminOut)
def update_admin(
        admin_id: int,
        admin: AdminUpdate,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = AdminService(db)
        return service.update(admin_id, admin)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{admin_id}", response_model=AdminOut)
def delete_admin(
        admin_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = AdminService(db)
        return service.delete(admin_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/{admin_id}/companies/{company_id}", response_model=AdminOut)
def create_m2m_admin_company(
        admin_id: int,
        company_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = AdminService(db)
        return service.add_company_to_admin(admin_id, company_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{admin_id}/companies/{company_id}", response_model=AdminOut)
def remove_m2m_admin_company(
        admin_id: int,
        company_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = AdminService(db)
        return service.remove_company_from_admin(admin_id, company_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/login", response_model=Token)
def login_for_admin_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    service = AdminService(db)
    admin = service.authenticate_admin(form_data.username, form_data.password)
    access_token = service.create_admin_token(admin)
    return {"access_token": access_token, "token_type": "bearer"}
