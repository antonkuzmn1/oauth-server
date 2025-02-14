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

from fastapi import FastAPI
from app.api.admins import router as admins_router
from app.api.companies import router as companies_router
from app.api.users import router as users_router
from app.core.settings import settings

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
