from typing import List, Optional, Type, TypeVar, Generic
from pydantic import BaseModel

from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


T = TypeVar("T", bound=BaseRepository)
SchemaOut = TypeVar("SchemaOut", bound=BaseModel)
SchemaBase = TypeVar("SchemaBase", bound=BaseModel)


class BaseService(Generic[T]):
    def __init__(self, repository: T, schema_out: Type[SchemaOut]):
        self.repository = repository
        self.schema_out = schema_out

    async def create(self, data: SchemaBase) -> SchemaOut:
        logger.warning("BASE_SERVICE: Attempt to create something")
        record = await self.repository.create(data.model_dump())
        return self.schema_out.model_validate(record)

    async def update(self, record_id: int, data: SchemaBase) -> Optional[SchemaOut]:
        logger.warning(f"BASE_SERVICE: Attempt to update record {record_id}")
        record = await self.repository.update(record_id, data.model_dump())

        if not record:
            logger.warning(f"BASE_SERVICE: Record {record_id} not found for update")
            return None

        return self.schema_out.model_validate(record)

    async def delete(self, record_id: int) -> Optional[SchemaOut]:
        record = await self.repository.delete(record_id)

        if not record:
            logger.warning(f"BASE_SERVICE: Record {record_id} not found for delete")
            return None

        return self.schema_out.model_validate(record)

    async def get_all(self, *filters, options=None) -> List[SchemaOut]:
        records = await self.repository.get_all(*filters, options=options)
        return [self.schema_out.model_validate(record) for record in records]

    async def get_by_id(self, record_id: int, *filters, options=None) -> Optional[SchemaOut]:
        record = await self.repository.get_by_id(record_id, *filters, options=options)

        if not record:
            logger.warning(f"BASE_SERVICE: Record {record_id} not found")
            return None

        return self.schema_out.model_validate(record)

    async def get_by_username(self, username: str, *filters, options=None) -> Optional[SchemaOut]:
        record = await self.repository.get_by_username(username, *filters, options=options)

        if not record:
            logger.warning(f"BASE_SERVICE: User {username} not found")
            return None

        return self.schema_out.model_validate(record)
