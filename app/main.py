"""
Copyright 2025 Anton Kuzmin (github.com/antonkuzmn1)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.admins import router as admins_router
from app.api.companies import router as companies_router
from app.api.users import router as users_router
from app.api.owner import router as owner_router
from app.api.config import router as config_router

from app.services.auth_service import AuthService

from app.core.settings import settings

from app.utils.startup import startup


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Server started!")
    startup()
    yield
    print("Server stopped!")


auth_service = AuthService()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admins_router)
app.include_router(companies_router)
app.include_router(users_router)
app.include_router(owner_router)
app.include_router(config_router)


@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
        "test": 16,
    }


@app.post("/check")
def check_token(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    return auth_service.verify_token(token)

