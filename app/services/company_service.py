from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyOut
from app.repositories.base_repo import BaseRepository
from app.services.base_service import BaseService


class CompanyService(BaseService):
    def __init__(self, db: Session):
        repo = BaseRepository(db, Company)
        super().__init__(repo, CompanyOut)
