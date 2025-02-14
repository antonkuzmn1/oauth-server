from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OwnerBase(BaseModel):
    username: str


class OwnerCreate(OwnerBase):
    password: str


class OwnerUpdate(OwnerBase):
    password: Optional[str] = None


class OwnerOut(OwnerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True