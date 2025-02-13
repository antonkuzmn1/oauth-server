from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.admins import router as admins_router
from app.api.companies import router as companies_router
from app.api.users import router as users_router
from app.core.config import settings

app = FastAPI()

app.include_router(admins_router)
app.include_router(companies_router)
app.include_router(users_router)


@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
        "test": 16,
    }
