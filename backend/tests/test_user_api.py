def test_root(test_client):
    response = test_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"message": "api is healthy"}


def test_create_get_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201
    print(response_json)

    response = test_client.get(f"/api/users/{response_json['User']['id']}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["User"]["username"] == user_payload["username"]
    assert response_json["User"]["email"] == user_payload["email"]
    assert response_json["User"]["user_type_id"] == user_payload["user_type_id"]


def test_create_delete_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201
    created_user_id = response_json["User"]["id"]

    response = test_client.delete(f"/api/users/{created_user_id}")
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["Message"] == "User deleted successfully"

    # Get the deleted user
    response = test_client.get(f"/api/users/{created_user_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert (
        response_json["detail"] == f"No User with this id: `{user_payload['id']}` found"
    )


def test_create_update_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201
    created_user_id = response_json["User"]["id"]

    user_payload["username"] = "updated"
    response = test_client.patch(f"/api/users/{created_user_id}", json=user_payload)
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["User"]["username"] == "updated"


def test_create_integrity(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    response = test_client.post("/api/users/", json=user_payload)
    assert response.status_code == 409
