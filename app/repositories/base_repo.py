from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, literal
from app.models import Base
from app.utils.logger import logger


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_username(self, username: str) -> Optional[T]:
        return self.db.scalar(select(self.model).where(
            self.model.username == username,
            self.model.deleted.is_(False))
        )

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def get_by_id(self, item_id: int) -> Optional[T]:
        return self.db.scalar(select(self.model).where(
            self.model.id == item_id,
            self.model.deleted.is_(False)))

    def create(self, item_data: dict) -> Optional[T]:
        logger.warning("BASE_REPO: Attempt to create something")
        item = self.model(**item_data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item_id: int, item_data: dict) -> Optional[T]:
        logger.warning("BASE_REPO: Attempt to update something")
        item = self.get_by_id(item_id)
        if not item:
            return None

        for key, value in item_data.items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> Optional[T]:
        item = self.get_by_id(item_id)
        if not item:
            return None

        item.deleted = True
        self.db.commit()
        return item
