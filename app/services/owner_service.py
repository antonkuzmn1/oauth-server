from sqlalchemy.orm import Session

from app.repositories.owner_repo import OwnerRepository
from app.schemas.owner import OwnerOut
from app.services.base_service import BaseService


class OwnerService(BaseService):
    def __init__(self, db: Session):
        repo = OwnerRepository(db)
        super().__init__(repo, OwnerOut)
