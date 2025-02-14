from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db


router = APIRouter(prefix="/owner", tags=["owner"])
