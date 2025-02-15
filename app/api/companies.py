from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependecies.auth import get_current_owner, get_current_admin, get_current_user
from app.schemas.admin import AdminOut
from app.schemas.company import CompanyOut, CompanyBase, CompanyCreate, CompanyUpdate
from app.schemas.owner import OwnerOut
from app.schemas.user import UserOut
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=List[CompanyOut])
def get_all_companies(
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    service = CompanyService(db)

    if current_owner:
        return service.get_all()

    if current_admin:
        return service.get_all_by_admin(current_admin)

    if current_user:
        return service.get_all_by_user(current_user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{company_id}", response_model=CompanyOut)
def get_company_by_id(
        company_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    service = CompanyService(db)

    if current_owner:
        return service.get_by_id(company_id)

    if current_admin:
        return service.get_by_id_by_admin(company_id, current_admin)

    if current_user:
        return service.get_by_id_by_user(company_id, current_user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=CompanyOut)
def create_company(
        company: CompanyCreate,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = CompanyService(db)
        return service.create(company)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{company_id}", response_model=CompanyOut)
def update_company(
        company_id: int,
        company: CompanyUpdate,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = CompanyService(db)
        return service.update(company_id, company)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{company_id}", response_model=CompanyOut)
def delete_company(
        company_id: int,
        db: Session = Depends(get_db),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        service = CompanyService(db)
        return service.delete(company_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
