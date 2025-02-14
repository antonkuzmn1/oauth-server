from sqlalchemy.orm import Session

from app.repositories.user_repo import UserRepository
from app.schemas.user import UserOut

from app.services.base_service import BaseService
from app.services.auth_service import AuthService


class UserService(BaseService[UserRepository]):
    def __init__(self, db: Session):
        super().__init__(UserRepository(db), UserOut)

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
