from typing import List, Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.company import Company
from app.repositories.base_repo import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: Session):
        super().__init__(db, Company)
