from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.admin import Admin
from app.models.company import admin_company_association, Company
from app.repositories.base_repo import BaseRepository

from app.utils.logger import logger



class AdminRepository(BaseRepository[Admin]):
    def __init__(self, db: Session):
        super().__init__(db, Admin)

    def get_all_admins_by_company(self, company_id: int) -> List[Admin]:
        try:
            admins = self.db.scalars(
                select(Admin)
                .join(admin_company_association)
                .where(admin_company_association.c.company_id == company_id)
            ).all()
            return list(admins)

        except SQLAlchemyError as e:
            logger.error(f"Error fetching admins by company: {e}")
            self.db.rollback()
            return []

    def get_all_companies_by_admin(self, admin_id: int) -> List[Company]:
        try:
            admin = self.db.scalar(
                select(Admin).where(
                    Admin.id == admin_id,
                    Admin.deleted.is_(False)
                )
            )
            return admin.companies if admin else []

        except SQLAlchemyError as e:
            logger.error(f"Error fetching companies by admin: {e}")
            self.db.rollback()
            return []

    def add_company_to_admin(self, admin_id: int, company_id: int) -> Optional[Admin]:
        try:
            admin = self.get_by_id(admin_id)
            company = self.db.scalar(select(Company).where(Company.id == company_id))

            if not admin or not company or company in admin.companies:
                return None

            admin.companies.append(company)
            self.db.commit()
            self.db.refresh(admin)
            return admin

        except SQLAlchemyError as e:
            logger.error(f"Error adding company to admin: {e}")
            self.db.rollback()
            return None

    def remove_company_from_admin(self, admin_id: int, company_id: int) -> Optional[Admin]:
        try:
            admin = self.get_by_id(admin_id)
            company = self.db.scalar(select(Company).where(Company.id == company_id))

            if not admin or not company or company not in admin.companies:
                return None

            admin.companies.remove(company)
            self.db.commit()
            self.db.refresh(admin)
            return admin

        except SQLAlchemyError as e:
            logger.error(f"Error removing company from admin: {e}")
            self.db.rollback()
            return None