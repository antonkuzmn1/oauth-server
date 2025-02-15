from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import Company
from app.repositories.company_repo import CompanyRepository
from app.schemas.admin import AdminOut
from app.schemas.company import CompanyOut, CompanyCreate, CompanyUpdate
from app.schemas.user import UserOut
from app.services.base_service import BaseService


class CompanyService(BaseService[CompanyRepository]):
    def __init__(self, db: Session):
        super().__init__(CompanyRepository(db), CompanyOut)
        self.db = db

    def get_all_by_admin(self, current_admin: AdminOut) -> List[CompanyOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return []

        stmt = (
            select(Company)
            .filter(Company.id.in_(company_ids))
            .distinct()
        )

        companies = self.db.scalars(stmt).all()
        return [CompanyOut.model_validate(company) for company in companies]

    def get_all_by_user(self, current_user: UserOut) -> Optional[CompanyOut]:
        company_id = current_user.company_id
        if not company_id:
            return None

        stmt = (
            select(Company)
            .filter(Company.id == company_id)
            .distinct()
        )
        company = self.db.scalars(stmt).first()
        return CompanyOut.model_validate(company) if company else None

    def get_by_id_by_admin(self, company_id: int, current_admin: AdminOut) -> Optional[CompanyOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return None

        stmt = (
            select(Company)
            .filter(Company.id.in_(company_ids))
            .filter(Company.id == company_id)
            .distinct()
        )

        company = self.db.scalars(stmt).first()
        return CompanyOut.model_validate(company) if company else None

    def get_by_id_by_user(self, company_id: int, current_user: UserOut) -> Optional[CompanyOut]:
        company_id = current_user.company_id
        if not company_id:
            return None

        stmt = (
            select(Company)
            .filter(Company.id == company_id)
            .distinct()
        )

        company = self.db.scalars(stmt).first()
        return CompanyOut.model_validate(company) if company else None
