from typing import Optional

from sqlalchemy.orm import Session

from app.models import Owner
from app.repositories.owner_repo import OwnerRepository
from app.schemas.owner import OwnerOut, OwnerCreate, OwnerUpdate
from app.services.auth_service import AuthService
from app.services.base_service import BaseService
from app.utils.logger import logger

auth_service = AuthService()


class OwnerService(BaseService[OwnerRepository]):
    def __init__(self, db: Session):
        super().__init__(OwnerRepository(db), OwnerOut)

    def create(self, owner_data: OwnerCreate) -> Optional[OwnerOut]:
        logger.warning("OWNER_SERVICE: Attempt to create owner")

        owner_data_dict = owner_data.model_dump(exclude={"password"})
        owner_data_dict["hashed_password"] = auth_service.hash_password(owner_data.password)

        return super().create(owner_data_dict)

    def update(self, owner_id: int, owner_data: OwnerUpdate) -> Optional[OwnerOut]:
        logger.warning("OWNER_SERVICE: Attempt to update owner")
        # noinspection DuplicatedCode
        owner = self.repository.get_by_id(owner_id)
        if not owner:
            logger.warning(f"Attempt to update non-existent owner: {owner_id}")
            return None

        updated_owner = owner_data.model_dump(exclude_unset=True)
        if "password" in updated_owner and updated_owner["password"]:
            updated_owner["hashed_password"] = auth_service.hash_password(updated_owner["password"])
            del updated_owner["password"]

        return super().update(owner_id, updated_owner)

    def authenticate_owner(self, username: str, password: str) -> Optional[Owner]:
        owner = self.repository.get_by_username(username)
        if not owner or not auth_service.verify_password(password, owner.hashed_password):
            return None
        return owner

    @classmethod
    def create_owner_token(cls, owner: Owner) -> Optional[str]:
        if not owner:
            return None
        token_data = {"sub": owner.username, "role": "owner", "id": owner.id}
        return auth_service.create_access_token(token_data)
