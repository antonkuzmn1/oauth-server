from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Company
from app.models.admin import admin_company_association
from app.repositories.company_repo import CompanyRepository
from app.schemas.admin import AdminOut
from app.schemas.company import CompanyOut
from app.schemas.user import UserOut
from app.services.base_service import BaseService


class CompanyService(BaseService[CompanyRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CompanyRepository(db), CompanyOut)

    async def get_all_companies_for_admin(self, current_admin: AdminOut) -> List[CompanyOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return []
        filters = [Company.id.in_(company_ids)]
        options = [selectinload(Company.admins)]
        return await super().get_all(*filters, options=options)

    async def get_company_for_user(self, current_user: UserOut) -> Optional[CompanyOut]:
        company_id = current_user.company_id
        if not company_id:
            return None
        options = [selectinload(Company.users)]
        return await super().get_by_id(company_id, options=options)

    async def get_company_by_id_for_admin(self, company_id: int, current_admin: AdminOut) -> Optional[CompanyOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return None
        filters = [admin_company_association.c.company_id.in_(company_ids)]
        options = [selectinload(Company.admins)]
        return await super().get_by_id(company_id, *filters, options=options)
