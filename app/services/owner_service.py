from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Owner
from app.repositories.owner_repo import OwnerRepository
from app.schemas.owner import OwnerOut, OwnerCreate, OwnerUpdate
from app.services.auth_service import AuthService
from app.services.base_service import BaseService
from app.utils.logger import logger


class OwnerService(BaseService[OwnerRepository]):
    def __init__(self, db: AsyncSession, auth_service: AuthService):
        super().__init__(OwnerRepository(db), OwnerOut)
        self.auth_service = auth_service

    async def create(self, owner_data: OwnerCreate) -> Optional[OwnerOut]:
        logger.warning("OWNER_SERVICE: Attempt to create owner")

        owner_data = owner_data.model_copy(
            update={"hashed_password": await self.auth_service.hash_password(owner_data.password)}
        )

        return await super().create(owner_data)

    async def update(self, owner_id: int, owner_data: OwnerUpdate) -> Optional[OwnerOut]:
        logger.warning("OWNER_SERVICE: Attempt to update owner")

        owner = await self.repository.get_by_id(owner_id)
        if not owner:
            logger.warning(f"Attempt to update non-existent owner: {owner_id}")
            return None

        update_data = owner_data.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = await self.auth_service.hash_password(update_data["password"])
            del update_data["password"]

        updated_owner = owner_data.model_copy(update=update_data)
        return await super().update(owner_id, updated_owner)

    async def authenticate_owner(self, username: str, password: str) -> Optional[Owner]:
        owner = await self.repository.get_by_username(username)
        if not owner or not await self.auth_service.verify_password(password, owner.hashed_password):
            return None
        return owner

    async def create_owner_token(self, owner: Owner) -> Optional[str]:
        if not owner:
            return None
        token_data = {"sub": owner.username, "role": "owner", "id": owner.id}
        return await self.auth_service.create_access_token(token_data)
