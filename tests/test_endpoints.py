def test_get_shows_view_requires_auth(test_client):
    response = test_client.get("/shows/")
    assert response.status_code == 401


def test_get_persons_view_requires_auth(test_client):
    response = test_client.get("/persons/")
    assert response.status_code == 401
