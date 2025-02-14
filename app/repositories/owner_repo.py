from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Owner
from app.repositories.base_repo import BaseRepository


class OwnerRepository(BaseRepository[Owner]):
    def __init__(self, db: Session):
        super().__init__(db, Owner)

    def get_by_username(self, username: str) -> Optional[Owner]:
        return self.db.scalar(select(Owner).where(Owner.username == username, Owner.deleted == False))

