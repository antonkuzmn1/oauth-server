from typing import Annotated, List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependecies.auth import get_current_owner
from app.schemas.config import ConfigOut, ConfigCreate, ConfigUpdate
from app.schemas.owner import OwnerOut
from app.services.config_service import ConfigService

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/", response_model=List[ConfigOut])
def get_all_configs(
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = ConfigService(db)
        return service.get_all()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{owner_id}", response_model=OwnerOut)
def get_config_by_key(
        config_key: str,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = ConfigService(db)
        return service.get_by_key(config_key)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=OwnerOut)
def create_owner(
        owner: ConfigCreate,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = ConfigService(db)
        return service.create(owner)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{config_key}", response_model=ConfigOut)
def update_owner(
        config_key: str,
        config: ConfigUpdate,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = ConfigService(db)
        return service.update(config_key, config)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{config_key}", response_model=OwnerOut)
def delete_owner(
        config_key: str,
        db: Session = Depends(get_db),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        service = ConfigService(db)
        return service.delete(config_key)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
