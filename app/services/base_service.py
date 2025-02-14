from typing import List, Optional, Type, TypeVar, Generic
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger

T = TypeVar("T", bound=BaseRepository)
SchemaOut = TypeVar("SchemaOut")
SchemaBase = TypeVar("SchemaBase")


class BaseService(Generic[T]):
    def __init__(self, repository: T, schema_out: Type[SchemaOut]):
        self.repository = repository
        self.schema_out = schema_out

    def create(self, data: SchemaBase) -> SchemaOut:
        logger.warning("BASE_SERVICE: Attempt to create something")

        if not isinstance(data, dict):
            data = data.model_dump()

        record = self.repository.create(data)
        return self.schema_out.model_validate(record)

    def update(self, record_id: int, data: SchemaBase) -> Optional[SchemaOut]:
        logger.warning("BASE_SERVICE: Attempt to update something")

        if not isinstance(data, dict):
            data = data.model_dump()

        record = self.repository.update(record_id, data)
        if record:
            return self.schema_out.model_validate(record)
        return None

    def delete(self, record_id: int) -> Optional[SchemaOut]:
        record = self.repository.delete(record_id)
        if record:
            return self.schema_out.model_validate(record)
        return None

    def get_all(self) -> List[SchemaOut]:
        records = self.repository.get_all()
        return [self.schema_out.model_validate(record) for record in records]

    def get_by_id(self, record_id: int) -> Optional[SchemaOut]:
        record = self.repository.get_by_id(record_id)
        if record:
            return self.schema_out.model_validate(record)
        return None