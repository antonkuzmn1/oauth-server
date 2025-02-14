from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependecies.auth import get_current_admin

from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from app.schemas.token import Token
from app.services.admin_service import AdminService


router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/", response_model=List[AdminOut])
def get_all_admins(db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.get_all()


@router.get("/profile", response_model=AdminOut)
async def get_admin_profile(current_admin: Annotated[AdminOut, Depends(get_current_admin)]):
    return current_admin


@router.get("/{admin_id}", response_model=AdminOut)
def get_admin_by_id(admin_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.get_by_id(admin_id)


@router.post("/", response_model=AdminOut)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.create(admin)


@router.put("/{admin_id}", response_model=AdminOut)
def update_admin(admin_id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.update(admin_id, admin)


@router.delete("/{admin_id}", response_model=AdminOut)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.delete(admin_id)


@router.post("/{admin_id}/companies/{company_id}", response_model=AdminOut)
def create_m2m_admin_company(admin_id: int, company_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.add_company_to_admin(admin_id, company_id)


@router.delete("/{admin_id}/companies/{company_id}", response_model=AdminOut)
def remove_m2m_admin_company(admin_id: int, company_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.remove_company_from_admin(admin_id, company_id)


@router.post("/login", response_model=Token)
def login_for_admin_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    service = AdminService(db)
    admin = service.authenticate_admin(form_data.username, form_data.password)
    access_token = service.create_admin_token(admin)
    return {"access_token": access_token, "token_type": "bearer"}