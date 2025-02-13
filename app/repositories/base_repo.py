from typing import Type, TypeVar, Generic, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, cast, Boolean
from app.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, item_id: int) -> Optional[T]:
        return self.db.scalar(select(self.model).where(
            cast(self.model.id, Boolean) == item_id,
            cast(self.model.deleted, Boolean) == False))

    def create(self, item_data: dict) -> T:
        item = self.model(**item_data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item_id: int, item_data: dict) -> Optional[T]:
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
