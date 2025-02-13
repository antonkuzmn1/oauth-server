from typing import Optional
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut
from app.services.auth_service import AuthService
from app.repositories.base_repo import BaseRepository
from app.services.base_service import BaseService
from app.services.company_service import CompanyService


auth_service = AuthService()


class AdminService(BaseService):
    def __init__(self, db: Session):
        repo = BaseRepository(db, Admin)
        super().__init__(repo, AdminOut)
        self.db = db

    def create(self, admin_data: AdminCreate) -> Optional[AdminOut]:
        hashed_password = auth_service.hash_password(admin_data.password)
        admin_data_dict = admin_data.model_dump(exclude={"password"})
        new_admin = self.repository.model(**admin_data_dict, hashed_password=hashed_password)
        self.db.add(new_admin)
        self.db.commit()
        self.db.refresh(new_admin)
        logger.info(f"Created new admin: {new_admin.id} - {new_admin.username}")
        return self.schema_out.from_orm(new_admin)

    def update(self, admin_id: int, admin_data: AdminUpdate) -> Optional[AdminOut]:
        admin = self.repository.get_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to update non-existent admin: {admin_id}")
            return None

        update_data = admin_data.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"] is not None:
            update_data["password"] = auth_service.hash_password(update_data["password"])
        update_data.pop("password", None)

        for key, value in update_data.items():
            setattr(admin, key, value)

        self.db.commit()
        self.db.refresh(admin)
        logger.info(f"Updated admin: {admin.id} - {admin.username}")
        return self.schema_out.from_orm(admin)

    def authenticate_admin(self, username: str, password: str):
        admin = self.repository.get_by_username(username)
        if not admin or not auth_service.verify_password(password, admin.hashed_password):
            return None
        return admin

    @classmethod
    def create_admin_token(cls, admin) -> str:
        token_data = {"sub": admin.username, "role": "admin"}
        return auth_service.create_access_token(token_data)
