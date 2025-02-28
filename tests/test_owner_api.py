# import pytest
# from fastapi import status
#
# @pytest.mark.asyncio
# async def test_get_owner_profile_unauthorized(client):
#     response = await client.get("/owner/profile")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_get_all_owners_unauthorized(client):
#     response = await client.get("/owner/")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_get_owner_by_id_unauthorized(client):
#     response = await client.get("/owner/1")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_create_owner_unauthorized(client):
#     payload = {
#         "username": "testowner",
#         "password": "testpass",
#     }
#     response = await client.post("/owner/", json=payload)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_update_owner_unauthorized(client):
#     payload = {
#         "username": "updatedowner",
#         "password": "updatedpass",
#     }
#     response = await client.put("/owner/1", json=payload)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_delete_owner_unauthorized(client):
#     response = await client.delete("/owner/1")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"
#
# @pytest.mark.asyncio
# async def test_login_owner_invalid_credentials(client):
#     response = await client.post("/owner/login", data={"username": "wrong", "password": "wrong"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid username or password"
