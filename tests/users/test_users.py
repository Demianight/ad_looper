from fastapi.testclient import TestClient


def test_get_users(client: TestClient, setup_database):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client: TestClient, setup_database):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]


def test_read_user(client: TestClient, setup_database):
    # First, create a user to test reading
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
    }
    create_response = client.post("/users", json=user_data)
    created_user_id = create_response.json()["id"]

    # Then, read the user
    response = client.get(f"/users/{created_user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == created_user_id
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]


def test_update_user(client: TestClient, setup_database):
    # First, create a user to test updating
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Update the user
    update_data = {
        "username": "updated_user",
        "email": "updated_user@example.com",
    }
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id
    assert response_data["username"] == update_data["username"]
    assert response_data["email"] == update_data["email"]


def test_delete_user(client: TestClient, setup_database):
    # First, create a user to test deletion
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify the user has been deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
