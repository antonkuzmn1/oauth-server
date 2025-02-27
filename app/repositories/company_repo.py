from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.repositories.base_repo import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Company)