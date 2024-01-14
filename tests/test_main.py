import asyncio
import random
import string

import pytest
from fastapi.testclient import TestClient

from app.database.database import engine, Base
from app.main import app


class TestMain:

    def setup_class(self) -> None:
        asyncio.run(self.init_bd(self))

    @pytest.mark.asyncio
    async def init_bd(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    client = TestClient(app)

    @pytest.fixture
    def user_json(self):
        return {
                    "name": "testuser",
                    "username": "testusername",
                    "email": ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)),
                    "password": "Test Password"
                }

    def test_health_check(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Health check"}

    def test_get_users(self):
        response = self.client.get("/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_user(self, user_json):
        response = self.client.post("/user/", json=user_json)
        user_id = response.json()["id"]

        response = self.client.get(f"/user/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    def test_create_user(self, user_json):
        response = self.client.post("/user/", json=user_json)
        assert response.status_code == 201
        assert "id" in response.json()

    def test_update_user(self, user_json):
        response = self.client.post("/user/", json=user_json)
        user_id = response.json()["id"]

        updated_data = {
                "name": "updated",
                "username": "updatedsd",
                "email": "updated@test.com",
                "password": "updated"
            }
        response = self.client.patch(f"/user/{user_id}", json=updated_data)

        assert response.status_code == 200
        assert response.json()["id"] == user_id
        assert response.json()["username"] == updated_data["username"]

    def test_delete_user(self, user_json):
        response = self.client.post("/user/", json=user_json)
        user_id = response.json()["id"]

        response = self.client.delete(f"/user/{user_id}")
        assert response.status_code == 200
