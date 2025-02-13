from datetime import datetime, UTC
from unittest.mock import MagicMock

import pytest

from app.models import Company
from app.schemas.company import CompanyBase
from app.services.company_service import CompanyService


@pytest.fixture
def db():
    db = MagicMock()
    db.refresh.side_effect = lambda obj: (
            setattr(obj, "id", 1) or
            setattr(obj, "created_at", datetime.now(UTC)) or
            setattr(obj, "updated_at", datetime.now(UTC))
    )
    return db


@pytest.fixture
def service(db):
    return CompanyService(db)


def test_create(service, db):
    db.add.return_value = True
    db.commit.return_value = True
    db.refresh.return_value = True

    company_data = CompanyBase(name="company")

    new_company = service.create(company_data)

    assert new_company.name == "company"
    assert new_company.id == 1
    assert new_company.created_at is not None
    assert new_company.updated_at is not None

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_update(service, db):
    company = Company(name="company")

    db.query.return_value.filter.return_value.first.return_value = company

    update_company = CompanyBase(name="updated company")
    updated_company = service.update(1, update_company)

    assert updated_company.name == "updated company"
    assert updated_company.description is None
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_delete(service, db):
    company = Company(name="company")

    db.query.return_value.filter.return_value.first.return_value = company

    deleted_company = service.delete(1)

    assert deleted_company.name == "company"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
