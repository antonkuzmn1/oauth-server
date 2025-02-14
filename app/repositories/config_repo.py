from typing import Optional

from sqlalchemy.orm import Session

from app.models import Config


class ConfigRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Config).all()

    def get_by_key(self, key: str) -> Optional[Config]:
        return self.db.query(Config).filter(Config.key == key).first()

    def create(self, key: str, value: str) -> Config:
        item = Config(key=key, value=value)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, key: str, value: str) -> Optional[Config]:
        item = self.get_by_key(key)
        if not item:
            return None

        setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, key: str) -> Optional[Config]:
        item = self.get_by_key(key)
        if not item:
            return None

        self.db.delete(item)
        self.db.commit()
        return item