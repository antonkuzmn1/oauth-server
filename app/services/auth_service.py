from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

from app.core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self,
                 secret_key: str = settings.SECRET_KEY,
                 algorithm: str = settings.ALGORITHM,
                 expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm or 'HS256')
        return token

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except PyJWTError:
            return None

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)