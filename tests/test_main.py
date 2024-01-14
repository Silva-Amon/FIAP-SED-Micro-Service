from fastapi.testclient import TestClient
from main import app


class TestMain:

    TEST_DB_URL = "sqlite:///../db.sqlite"

    client = TestClient(app)

    user_json = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass",
                "full_name": "Test User"
            }

    # app.dependency_overrides[database.fetch_all] = []

    def test_health_check(self):
        response = self.client.get("/health-check")
        assert response.status_code == 200
        assert response.json() == {"message": "Health check"}

    def test_get_users(self):
        response = self.client.get("/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_user(self):
        response = self.client.post("/user/", json=self.user_json)
        user_id = response.json()["id"]

        response = self.client.get(f"/user/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    def test_create_user(self):
        response = self.client.post("/user/", json=self.user_json)
        assert response.status_code == 200
        assert "id" in response.json()

    def test_update_user(self):
        response = self.client.post("/user/", json=self.user_json)
        user_id = response.json()["id"]

        updated_data = {"username": "updateduser", "email": "updated@example.com", "password": "updatedpass", "full_name": "Updated User"}
        response = self.client.put(f"/user/{user_id}", json=updated_data)

        assert response.status_code == 200
        assert response.json()["id"] == user_id
        assert response.json()["username"] == updated_data["username"]

    def test_delete_user(self):
        response = self.client.post("/user/", json=self.user_json)
        user_id = response.json()["id"]

        response = self.client.delete(f"/user/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id
