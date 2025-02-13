from sqlalchemy import Column, Integer, String, DateTime, func, Boolean

from app.models import Base


class Config(Base):
    __tablename__ = 'config'

    key = Column(String(50), primary_key=True)
    value = Column(String(50), nullable=False, default='')
