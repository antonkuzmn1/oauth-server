from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel


class CompanyBase(BaseModel):
    username: str
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
