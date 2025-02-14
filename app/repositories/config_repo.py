from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models import Config
from app.utils.logger import logger


class ConfigRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        try:
            return self.db.query(Config).all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get all configs: {e}")
            self.db.rollback()
            return []

    def get_by_key(self, key: str) -> Optional[Config]:
        try:
            return self.db.query(Config).filter(Config.key == key).first()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get config by key={key}: {e}")
            self.db.rollback()
            return None

    def create(self, key: str, value: str) -> Optional[Config]:
        try:
            item = Config(key=key, value=value)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to create config key={key}: {e}")
            self.db.rollback()
            return None

    def update(self, key: str, value: str) -> Optional[Config]:
        try:
            item = self.get_by_key(key)
            if not item:
                return None

            item.value = value
            self.db.commit()
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to update config key={key}: {e}")
            self.db.rollback()
            return None

    def delete(self, key: str) -> Optional[Config]:
        try:
            item = self.get_by_key(key)
            if not item:
                return None

            self.db.delete(item)
            self.db.commit()
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete config key={key}: {e}")
            self.db.rollback()
            return None