from app.core.db import SessionLocal
from app.schemas.owner import OwnerCreate
from app.services.owner_service import OwnerService

def create_owner_if_not_exists():
    db = SessionLocal()
    service = OwnerService(db)
    owner = service.get_by_id(1)
    if not owner:
        owner = OwnerCreate(username='owner', password='owner')
        service.create(owner)
        print('Owner created')

def startup():
    create_owner_if_not_exists()
