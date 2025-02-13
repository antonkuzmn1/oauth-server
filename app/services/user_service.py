from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserOut
from app.repositories.base_repo import BaseRepository
from app.services.base_service import BaseService
from app.services.auth_service import AuthService


class UserService(BaseService):
    def __init__(self, db: Session):
        repo = BaseRepository(db, User)
        super().__init__(repo, UserOut)
        self.db = db

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
