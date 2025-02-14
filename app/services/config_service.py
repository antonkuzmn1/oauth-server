from typing import List, Optional

from sqlalchemy.orm import Session

from app.repositories.config_repo import ConfigRepository
from app.schemas.config import ConfigOut, ConfigCreate, ConfigUpdate


class ConfigService:
    def __init__(self, db: Session):
        repo = ConfigRepository(db)
        self.db = db
        self.repository = repo
        self.schema_out = ConfigOut

    def get_all(self) -> List[ConfigOut]:
        records = self.repository.get_all()
        return [self.schema_out.model_validate(record) for record in records]

    def get_by_key(self, key: str) -> Optional[ConfigOut]:
        record = self.repository.get_by_key(key)
        if record:
            return self.schema_out.model_validate(record)
        return None

    def create(self, config: ConfigCreate) -> ConfigOut:
        record = self.repository.create(key=config.key, value=config.value)
        return self.schema_out.model_validate(record)

    def update(self, config: ConfigUpdate) -> Optional[ConfigOut]:
        record = self.repository.update(key=config.key, value=config.value)
        if record:
            return self.schema_out.model_validate(record)
        return None

    def delete(self, key: str) -> Optional[ConfigOut]:
        record = self.repository.delete(key=key)
        if record:
            return self.schema_out.model_validate(record)
        return None
