import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_profile(client: AsyncClient):
    response = await client.get("/users/profile")
    assert response.status_code in [200, 401]

@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code in [200, 401]

@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient):
    user_id = 1
    response = await client.get(f"/users/{user_id}")
    assert response.status_code in [200, 401, 404]

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    new_user = {
        "username": "testuser",
        "password": "securepassword",
        "name": "testname",
        "surname": "testsurname",
        "company_id": "1"
    }
    response = await client.post("/users/", json=new_user)
    assert response.status_code in [201, 401]

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    user_id = 1
    update_data = {
        "username": "updateuser",
        "password": "updatesecurepassword",
        "name": "updatename",
        "surname": "updatesurname",
        "company_id": "2"
    }
    response = await client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code in [200, 401, 403, 404]

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    user_id = 1
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code in [200, 401, 403, 404]

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    login_data = {"username": "testuser", "password": "securepassword"}
    response = await client.post("/users/login", data=login_data)
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        assert "access_token" in response.json()
