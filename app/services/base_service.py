from typing import List, Optional, Type, TypeVar, Generic
from app.repositories.base_repo import BaseRepository


T = TypeVar("T", bound=BaseRepository)
SchemaOut = TypeVar("SchemaOut")
SchemaBase = TypeVar("SchemaBase")


class BaseService(Generic[T]):
    def __init__(self, repository: T, schema_out: Type[SchemaOut]):
        self.repository = repository
        self.schema_out = schema_out

    def get_all(self) -> List[SchemaOut]:
        records = self.repository.get_all()
        return [self.schema_out.from_orm(record) for record in records]

    def get_by_id(self, record_id: int) -> Optional[SchemaOut]:
        record = self.repository.get_by_id(record_id)
        if record:
            return self.schema_out.from_orm(record)
        return None

    def create(self, data: SchemaBase) -> SchemaOut:
        record = self.repository.create(data)
        return self.schema_out.from_orm(record)

    def update(self, record_id: int, data: SchemaBase) -> Optional[SchemaOut]:
        record = self.repository.update(record_id, data)
        if record:
            return self.schema_out.from_orm(record)
        return None

    def delete(self, record_id: int) -> Optional[SchemaOut]:
        record = self.repository.delete(record_id)
        if record:
            return self.schema_out.from_orm(record)
        return None
