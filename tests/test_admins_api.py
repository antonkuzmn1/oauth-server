# import pytest
# from httpx import AsyncClient
# from fastapi import status
#
#
# @pytest.mark.asyncio
# async def test_get_admin_profile_unauthorized(client: AsyncClient, stub_admin_auth):
#     response = await client.get("/admins/profile")
#     assert response.status_code == status.HTTP_200_OK
#
# @pytest.mark.asyncio
# async def test_get_all_admins_unauthorized(client: AsyncClient):
#     response = await client.get("/admins/")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_get_admin_by_id_unauthorized(client: AsyncClient):
#     response = await client.get("/admins/1")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_create_admin_unauthorized(client: AsyncClient):
#     payload = {"username": "testadmin",
#                "name": "nameadmin",
#                "surname": "surnameadmin",
#                "password": "testpass"}
#     response = await client.post("/admins/", json=payload)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_update_admin_unauthorized(client: AsyncClient):
#     payload = {"username": "testadmin2",
#                "name": "nameadmin2",
#                "surname": "surnameadmin2",
#                "password": "testpass2"}
#     response = await client.put("/admins/1", json=payload)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_delete_admin_unauthorized(client: AsyncClient):
#     response = await client.delete("/admins/1")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_create_m2m_admin_company_unauthorized(client: AsyncClient):
#     response = await client.post("/admins/1/companies/1")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_remove_m2m_admin_company_unauthorized(client: AsyncClient):
#     response = await client.delete("/admins/1/companies/1")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_login_admin_invalid_credentials(client: AsyncClient):
#     response = await client.post("/admins/login", data={"username": "wrong", "password": "wrong"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid username or password"
