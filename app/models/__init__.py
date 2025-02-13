from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.company import Company
from app.models.user import User
from app.models.admin import Admin

