from typing import Annotated, Optional, List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependecies.auth import get_current_owner
from app.schemas.owner import OwnerOut, OwnerCreate, OwnerUpdate
from app.schemas.token import Token
from app.services.owner_service import OwnerService

router = APIRouter(prefix="/owner", tags=["owner"])


@router.get("/profile", response_model=OwnerOut)
async def get_owner_profile(
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)],
):
    if current_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return current_owner


@router.get("/", response_model=List[OwnerOut])
def get_all_owners(
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = OwnerService(db)
        return service.get_all()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{owner_id}", response_model=OwnerOut)
def get_owner_by_id(
        owner_id: int,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = OwnerService(db)
        return service.get_by_id(owner_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=OwnerOut)
def create_owner(
        owner: OwnerCreate,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = OwnerService(db)
        return service.create(owner)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{owner_id}", response_model=OwnerOut)
def update_owner(
        owner_id: int,
        owner: OwnerUpdate,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = OwnerService(db)
        return service.update(owner_id, owner)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{owner_id}", response_model=OwnerOut)
def delete_owner(
        owner_id: int,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = OwnerService(db)
        return service.delete(owner_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/login", response_model=Optional[Token])
def login_for_owner_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    service = OwnerService(db)
    owner = service.authenticate_owner(form_data.username, form_data.password)

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = service.create_owner_token(owner)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return {"access_token": access_token, "token_type": "Bearer"}
