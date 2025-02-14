from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.admin_repo import AdminRepository
from app.utils.logger import logger
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut
from app.services.auth_service import AuthService
from app.services.base_service import BaseService

auth_service = AuthService()


class AdminService(BaseService[AdminRepository]):
    def __init__(self, db: Session):
        super().__init__(AdminRepository(db), AdminOut)

    def create(self, admin_data: AdminCreate) -> Optional[AdminOut]:
        hashed_password = auth_service.hash_password(admin_data.password)
        admin_data_dict = admin_data.model_dump(exclude={"password"})
        new_admin = Admin(**admin_data_dict, hashed_password=hashed_password)

        self.repository.db.add(new_admin)
        self.repository.db.commit()
        self.repository.db.refresh(new_admin)

        logger.info(f"Created new admin: {new_admin.id} - {new_admin.username}")
        return AdminOut.model_validate(new_admin)

    def update(self, admin_id: int, admin_data: AdminUpdate) -> Optional[AdminOut]:
        admin = self.repository.get_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to update non-existent admin: {admin_id}")
            return None

        update_data = admin_data.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password"] = auth_service.hash_password(update_data["password"])

        for key, value in update_data.items():
            setattr(admin, key, value)

        self.repository.db.commit()
        self.repository.db.refresh(admin)

        logger.info(f"Updated admin: {admin.id} - {admin.username}")
        return AdminOut.model_validate(admin)

    def add_company_to_admin(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.repository.add_company_to_admin(admin_id, company_id)
        return AdminOut.model_validate(admin) if admin else None

    def remove_company_from_admin(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.repository.remove_company_from_admin(admin_id, company_id)
        return AdminOut.model_validate(admin) if admin else None

    def authenticate_admin(self, username: str, password: str) -> Optional[Admin]:
        admin = self.repository.get_by_username(username)
        if not admin or not auth_service.verify_password(password, admin.hashed_password):
            return None
        return admin

    @classmethod
    def create_admin_token(cls, admin: Admin) -> str:
        token_data = {"sub": admin.id, "role": "admin"}
        return auth_service.create_access_token(token_data)
