from datetime import datetime, UTC
from unittest.mock import MagicMock

import pytest

from app.models import User
from app.schemas.user import UserBase
from app.services.user_service import UserService


@pytest.fixture
def company_mock():
    company = MagicMock()
    company.id = 1
    company.name = "Test Company"
    company.description = "Description of Test Company"
    return company


@pytest.fixture
def db(company_mock):
    db = MagicMock()
    db.refresh.side_effect = lambda obj: (
            setattr(obj, "id", 1) or
            setattr(obj, "created_at", datetime.now(UTC)) or
            setattr(obj, "updated_at", datetime.now(UTC)) or
            setattr(obj, "company", company_mock)
    )
    return db


@pytest.fixture
def service(db):
    return UserService(db)


def test_create(service, db):
    db.add.return_value = True
    db.commit.return_value = True
    db.refresh.return_value = True

    company_mock = MagicMock()
    company_mock.id = 1
    company_mock.name = "Test Company"
    company_mock.description = "Description of Test Company"

    data = UserBase(
        username="user",
        password="securepassword",
        surname="surname",
        name="name",
        company_id=company_mock.id,
    )

    entity = service.create(data)

    assert entity.username == "user"
    assert entity.surname == "surname"
    assert entity.company.id == company_mock.id

    db.commit.assert_called_once()
    db.refresh.assert_called_once()

    assert entity.surname == "surname"


def test_update(service, db):
    data = User(
        id=1,
        username="user",
        password="securepassword",
        surname="surname",
        name="name",
        company_id=1,
    )

    db.query.return_value.filter.return_value.first.return_value = data

    updated_data = UserBase(
        username="user",
        password="securepassword",
        surname="new_surname",
        name="name",
        company_id=1,
    )
    updated_entity = service.update(1, updated_data)

    assert updated_entity.surname == "new_surname"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_delete(service, db):
    data = User(
        id=1,
        username="user",
        password="securepassword",
        surname="surname",
        name="name",
        company_id=1,
    )

    db.query.return_value.filter.return_value.first.return_value = data

    deleted_entity = service.delete(1)

    assert deleted_entity.username == "user"
    db.query.assert_called_once()
    db.commit.assert_called_once()
