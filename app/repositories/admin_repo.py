from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, cast, Boolean
from app.models.admin import Admin
from app.models.company import admin_company_association, Company
from app.repositories.base_repo import BaseRepository
from app.schemas.admin import AdminOut


class AdminRepository(BaseRepository[Admin]):
    def __init__(self, db: Session):
        super().__init__(db, Admin)

    def get_by_username(self, username: str) -> Optional[Admin]:
        return self.db.scalar(select(Admin).where(Admin.username == username, Admin.deleted == False))

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

    def add_company_to_admin(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.db.scalar(select(Admin).where(Admin.id == admin_id, Admin.deleted == False))
        company = self.db.scalar(select(Company).where(Company.id == company_id))

        if not admin or not company:
            return None

        if company not in admin.companies:
            admin.companies.append(company)
            self.db.commit()
            self.db.refresh(admin)
        return admin

    def remove_company_from_admin(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.db.scalar(select(Admin).where(Admin.id == admin_id, Admin.deleted == False))
        company = self.db.scalar(select(Company).where(Company.id == company_id))

        if not admin or not company:
            return None

        if company in admin.companies:
            admin.companies.remove(company)
            self.db.commit()
            self.db.refresh(admin)
        return admin
