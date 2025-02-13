from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, cast, Boolean
from app.models.admin import Admin
from app.models.company import admin_company_association, Company
from app.repositories.base_repo import BaseRepository


class AdminRepository(BaseRepository[Admin]):
    def __init__(self, db: Session):
        super().__init__(db, Admin)

    def get_all_admins_by_company(self, company_id: int) -> List[Admin]:
        return list(self.db.scalars(
            select(Admin).join(admin_company_association).where(
                cast(admin_company_association.c.company_id, Boolean) == company_id)
        ).all())

    def get_all_companies_by_admin(self, admin_id: int) -> List[Company]:
        admin = self.db.scalar(
            select(Admin).where(Admin.id == admin_id, Admin.deleted == False)
        )
        if admin:
            return admin.companies
        return []