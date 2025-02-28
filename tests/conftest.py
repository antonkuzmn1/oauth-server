import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.dependencies.auth import get_current_user, get_current_admin, get_current_owner
from app.models import Company, User

from app.schemas.admin import AdminOut
from app.schemas.owner import OwnerOut
from app.schemas.user import UserOut
from app.schemas.company import CompanyOut

from app.core.db import Base
from app.core.db import get_db


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine = create_async_engine(TEST_DATABASE_URL, echo=True)


TestSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="function")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        company = Company(username="TestCompany", description="Test Company")
        session.add(company)
        await session.commit()
        await session.refresh(company)

        user = User(username="TestUser", name="Test User",
                    surname="TestSurname", password="testpassword",
                    company_id=1)
        session.add(user)
        await session.commit()
        await session.refresh(user)

        yield session


    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(test_db):
    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def role_fixture(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
async def stub_user_auth():
    async def override_get_current_user():
        return UserOut(
            username="testuser",
            surname="testsurname",
            name="testname",
            company_id=1,
            password="testpassword",
            id=1,
            company=CompanyOut(
                username="testcompany",
                description="testdescription",
                id=1
            )
        )

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
async def stub_admin_auth():
    async def override_get_current_admin():
        return AdminOut(
            username="testadmin",
            surname="testsurname",
            name="testname",
            id=1,
            companies=[
                CompanyOut(
                    username="testcompany",
                    description="testdescription",
                    id=1
                )
            ]
        )

    app.dependency_overrides[get_current_admin] = override_get_current_admin
    yield
    app.dependency_overrides.pop(get_current_admin, None)


@pytest.fixture
async def stub_owner_auth():
    async def override_get_current_owner():
        return OwnerOut(
            username="testowner",
            id=1
        )

    app.dependency_overrides[get_current_owner] = override_get_current_owner
    yield
    app.dependency_overrides.pop(get_current_owner, None)
