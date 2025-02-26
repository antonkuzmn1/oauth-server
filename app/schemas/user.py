from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.company import CompanyOut


class UserBase(BaseModel):
    username: str
    surname: str
    name: str
    middlename: Optional[str] = None
    department: Optional[str] = None
    remote_workplace: Optional[str] = None
    local_workplace: Optional[str] = None
    phone: Optional[str] = None
    cellular: Optional[str] = None
    post: Optional[str] = None
    company_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    surname: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    company_id: Optional[int] = None


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    company: CompanyOut

    model_config = ConfigDict(from_attributes=True)