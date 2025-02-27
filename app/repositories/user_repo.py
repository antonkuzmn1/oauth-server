from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models import Company
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User, default_options=[selectinload(User.company)])

    async def get_all_users_by_company(self, company_id: int) -> List[User]:
        try:
            filters = [User.company_id == company_id, User.deleted.is_(False)]
            return await self.get_all(*filters)
        except SQLAlchemyError as e:
            logger.error(f"Failed to get users by company_id={company_id}: {e}")
            await self.db.rollback()
            return []

    async def get_company_by_user_username(self, username: str) -> Optional[Company]:
        try:
            user = await self.get_by_username(username)
            return user.company if user else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get company by username={username}: {e}")
            await self.db.rollback()
            return None

    async def get_company_by_user_id(self, user_id: int) -> Optional[Company]:
        try:
            user = await self.get_by_id(user_id)
            return user.company if user else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get company by user_id={user_id}: {e}")
            await self.db.rollback()
            return None
