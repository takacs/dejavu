def test_root(test_client):
    response = test_client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "api is healthy"}


def test_create_get_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    assert response.status_code == 201
