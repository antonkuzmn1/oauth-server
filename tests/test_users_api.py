import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_200_OK),
    ("stub_admin_auth", status.HTTP_403_FORBIDDEN),
    ("stub_owner_auth", status.HTTP_403_FORBIDDEN),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_get_user_profile(client: AsyncClient, role_fixture, expected_status):
    response = await client.get("/users/profile")
    assert response.status_code == expected_status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_200_OK),
    ("stub_admin_auth", status.HTTP_200_OK),
    ("stub_owner_auth", status.HTTP_200_OK),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient, role_fixture, expected_status):
    response = await client.get("/users/")
    assert response.status_code == expected_status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_200_OK),
    ("stub_admin_auth", status.HTTP_200_OK),
    ("stub_owner_auth", status.HTTP_200_OK),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, role_fixture, expected_status):
    user_id = 1
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == expected_status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_403_FORBIDDEN),
    ("stub_admin_auth", status.HTTP_200_OK),
    ("stub_owner_auth", status.HTTP_200_OK),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, role_fixture, expected_status):
    new_user = {
        "username": "testuser",
        "password": "securepassword",
        "name": "testname",
        "surname": "testsurname",
        "company_id": "1"
    }
    response = await client.post("/users/", json=new_user)
    assert response.status_code == expected_status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_403_FORBIDDEN),
    ("stub_admin_auth", status.HTTP_200_OK),
    ("stub_owner_auth", status.HTTP_200_OK),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, role_fixture, expected_status):
    user_id = 1
    update_data = {
        "username": "updateuser",
        "password": "updatesecurepassword",
        "name": "updatename",
        "surname": "updatesurname",
        "company_id": "1"
    }
    response = await client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == expected_status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_403_FORBIDDEN),
    ("stub_admin_auth", status.HTTP_200_OK),
    ("stub_owner_auth", status.HTTP_200_OK),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, role_fixture, expected_status):
    user_id = 1
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == expected_status


@pytest.mark.parametrize("role_fixture, expected_status", [
    ("stub_user_auth", status.HTTP_403_FORBIDDEN),
    ("stub_admin_auth", status.HTTP_403_FORBIDDEN),
    ("stub_owner_auth", status.HTTP_403_FORBIDDEN),
], indirect=["role_fixture"])
@pytest.mark.asyncio
async def test_login(client: AsyncClient, role_fixture, expected_status):
    login_data = {"username": "testuser", "password": "testpassword"}
    response = await client.post("/users/login", data=login_data)
    assert response.status_code == expected_status