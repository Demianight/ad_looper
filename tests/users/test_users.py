from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "password": "testpass",
            "email": "test@email.com",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"


def test_read_current_user(client: TestClient):
    # Forbidden to read the current user without authentication
    response = client.get("/users/me")
    assert response.status_code == 403


def test_read_user(client: TestClient):
    # Create a user first
    user_data = {"username": "testuser", "password": "testpass"}
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Read the created user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_update_user(client: TestClient):
    # Create a user first
    user_data = {"username": "testuser", "password": "testpass"}
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Update the created user
    update_data = {"username": "updateduser"}
    response = client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"


def test_delete_user(client: TestClient):
    # Create a user first
    user_data = {"username": "testuser", "password": "testpass"}
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the created user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify the user is deleted
    read_response = client.get(f"/users/{user_id}")
    assert read_response.status_code == 404
