from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Company
from app.models.user import User
from app.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.scalar(select(User).where(User.username == username, User.deleted == False))

    def get_all_users_by_company(self, company_id: int) -> List[User]:
        return list(self.db.scalars(select(User).where(User.company_id == company_id, User.deleted == False)).all())

    def get_company_by_user_username(self, username: str) -> Optional[Company]:
        return self.db.scalar(select(User).where(User.username == username, User.deleted == False)).company
