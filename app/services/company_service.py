from sqlalchemy.orm import Session

from app.repositories.company_repo import CompanyRepository
from app.schemas.company import CompanyOut
from app.services.base_service import BaseService


class CompanyService(BaseService):
    def __init__(self, db: Session):
        repo = CompanyRepository(db)
        super().__init__(repo, CompanyOut)
