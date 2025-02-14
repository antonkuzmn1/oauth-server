from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Company
from app.models.user import User
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_all_users_by_company(self, company_id: int) -> List[User]:
        try:
            return list(self.db.scalars(select(User).where(
                User.company_id == company_id, User.deleted == False
            )).all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get users by company_id={company_id}: {e}")
            self.db.rollback()
            return []

    def get_company_by_user_username(self, username: str) -> Optional[Company]:
        try:
            user = self.db.scalar(select(User).where(User.username == username, User.deleted == False))
            return user.company if user else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get company by username={username}: {e}")
            self.db.rollback()
            return None

    def get_company_by_user_id(self, user_id: int) -> Optional[Company]:
        try:
            user = self.db.scalar(select(User).where(User.id == user_id, User.deleted == False))
            return user.company if user else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get company by user_id={user_id}: {e}")
            self.db.rollback()
            return None