from typing import Type, TypeVar, Generic, Optional, List, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.abstract_repo import AbstractRepository
from app.models import Base
from app.utils.logger import logger

T = TypeVar("T", bound=Base)


class BaseRepository(AbstractRepository[T], Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T], default_options: Sequence = ()):
        self.db = db
        self.model = model
        self.default_options = default_options

    def _apply_options(self, stmt, options):
        return stmt.options(*(options or self.default_options))

    async def get_by_username(self, username: str, *filters, options=None) -> Optional[T]:
        base_filters = [self.model.username == username, self.model.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = select(self.model).where(*base_filters)
        stmt = self._apply_options(stmt, options)
        return await self.db.scalar(stmt)

    async def get_all(self, *filters, options=None) -> List[T]:
        base_filters = [self.model.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = select(self.model).where(*base_filters).distinct()
        stmt = self._apply_options(stmt, options)
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, item_id: int, *filters, options=None) -> Optional[T]:
        base_filters = [self.model.id == item_id, self.model.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = select(self.model).where(*base_filters)
        stmt = self._apply_options(stmt, options)
        return await self.db.scalar(stmt)

    async def create(self, item_data: dict) -> Optional[T]:
        logger.warning(f"BASE_REPO: Creating {self.model.__name__} with data {item_data}")
        item = self.model(**item_data)
        try:
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            await self.db.rollback()
            return None

    async def update(self, item_id: int, item_data: dict) -> Optional[T]:
        logger.warning(f"BASE_REPO: Updating {self.model.__name__} with ID {item_id}")
        item = await self.get_by_id(item_id)
        if not item:
            return None

        for key, value in item_data.items():
            setattr(item, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Error updating {self.model.__name__}: {e}")
            await self.db.rollback()
            return None

    async def delete(self, item_id: int) -> Optional[T]:
        logger.warning(f"BASE_REPO: Deleting {self.model.__name__} with ID {item_id}")
        item = await self.get_by_id(item_id)
        if not item:
            return None

        item.deleted = True

        try:
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            return None
