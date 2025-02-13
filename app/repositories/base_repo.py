from typing import List, Optional, Type, TypeVar, cast
from sqlalchemy.orm import Session
from app.utils.logger import logger

T = TypeVar("T")
SchemaBase = TypeVar("SchemaBase")


class BaseRepository:
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def get_by_username(self, username: str) -> Optional[T]:
        return self.db.query(self.model).filter(
            cast("ColumnElement[bool]", self.model.username == username)
        ).first()

    def get_by_id(self, record_id: int) -> Optional[T]:
        return self.db.query(self.model).filter(
            cast("ColumnElement[bool]", self.model.id == record_id)
        ).first()

    def create(self, data: SchemaBase) -> T:
        new_record = self.model(**data.dict())
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        logger.info(f"Created new {self.model.__name__}: {new_record.id}")
        return new_record

    def update(self, record_id: int, data: SchemaBase) -> Optional[T]:
        record = self.get_by_id(record_id)
        if not record:
            logger.warning(f"Attempt to update non-existent {self.model.__name__}: {record_id}")
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        self.db.commit()
        self.db.refresh(record)
        logger.info(f"Updated {self.model.__name__}: {record.id}")
        return record

    def delete(self, record_id: int) -> Optional[T]:
        record = self.get_by_id(record_id)
        if not record:
            logger.warning(f"Attempt to delete non-existent {self.model.__name__}: {record_id}")
            return None

        setattr(record, "deleted", True)
        self.db.commit()
        self.db.refresh(record)
        logger.info(f"{self.model.__name__} marked as deleted: {record.id}")
        return record
