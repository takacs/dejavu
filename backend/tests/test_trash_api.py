def test_create_trash(test_client, trash_payload):
    response = test_client.post("/api/trash/", json=trash_payload)
    assert response.status_code == 201
