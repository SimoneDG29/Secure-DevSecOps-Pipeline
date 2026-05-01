from app import app

def test_auth_endpoint():
    client = app.test_client()
    response = client.post("/auth")
    assert response.status_code == 200
    assert response.get_json() == {"message": "User authenticated successfully"}

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}