from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.admin import AdminOut
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.services.auth_service import AuthService
from app.services.base_service import BaseService


class UserService(BaseService[UserRepository]):
    def __init__(self, db: Session):
        super().__init__(UserRepository(db), UserOut)
        self.db = db

    def get_all_by_admin(self, current_admin: AdminOut) -> List[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return []

        stmt = (
            select(User)
            .filter(User.company_id.in_(company_ids))
            .distinct()
        )
        users = self.db.scalars(stmt).all()
        return [UserOut.model_validate(user) for user in users]

    def get_all_by_user(self, current_user: UserOut) -> List[UserOut]:
        company_id = current_user.company_id
        if not company_id:
            return []

        stmt = (
            select(User)
            .filter(User.company_id == company_id)
            .distinct()
        )
        users = self.db.scalars(stmt).all()
        return [UserOut.model_validate(user) for user in users]

    def get_by_id_by_admin(self, user_id: int, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return None

        stmt = (
            select(User)
            .filter(User.company_id.in_(company_ids))
            .filter(User.id == user_id)
            .distinct()
        )

        user = self.db.scalars(stmt).first()
        return UserOut.model_validate(user) if user else None

    def get_by_id_by_user(self, user_id: int, current_user: UserOut) -> Optional[AdminOut]:
        company_id = current_user.company_id
        if not company_id:
            return None

        stmt = (
            select(User)
            .filter(User.company_id == company_id)
            .filter(User.id == user_id)
            .distinct()
        )

        user = self.db.scalars(stmt).first()
        return UserOut.model_validate(user) if user else None

    def create_by_admin(self, user: UserCreate, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]

        if not user.company_id or user.company_id not in company_ids:
            return None

        return self.create(user)

    def update_by_admin(self, user_id: int, user: UserUpdate, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        old_company_id = self.get_by_id(user_id).company_id

        if not old_company_id or old_company_id not in company_ids:
            return None

        if not user.company_id or user.company_id not in company_ids:
            return None

        return self.update(user_id, user)

    def delete_by_admin(self, user_id: int, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        old_company_id = self.get_by_id(user_id).company_id

        if not old_company_id or old_company_id not in company_ids:
            return None

        return self.delete(user_id)

    def authenticate_user(self, username: str, password: str):
        user = self.repository.get_by_username(username)
        if not user or user.password != password:
            return None
        return user

    @staticmethod
    def create_user_token(user) -> str:
        auth_service = AuthService()
        token_data = {"sub": user.username, "role": "user"}
        return auth_service.create_access_token(token_data)
