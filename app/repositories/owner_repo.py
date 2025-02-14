from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Owner
from app.repositories.base_repo import BaseRepository


class OwnerRepository(BaseRepository[Owner]):
    def __init__(self, db: Session):
        super().__init__(db, Owner)