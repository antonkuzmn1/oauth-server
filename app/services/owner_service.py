from sqlalchemy.orm import Session
from typing import Optional

from app.models import Owner
from app.repositories.owner_repo import OwnerRepository
from app.schemas.owner import OwnerOut
from app.services.auth_service import AuthService
from app.services.base_service import BaseService


auth_service = AuthService()


class OwnerService(BaseService[OwnerRepository]):
    def __init__(self, db: Session):
        super().__init__(OwnerRepository(db), OwnerOut)

    def authenticate_owner(self, username: str, password: str) -> Optional[OwnerOut]:
        owner = self.repository.get_by_username(username)
        if not owner or not auth_service.verify_password(password, owner.hashed_password):
            return None
        return owner

    @classmethod
    def create_owner_token(cls, owner: Owner) -> str:
        token_data = {"sub": owner.username, "role": "owner"}
        return auth_service.create_access_token(token_data)
