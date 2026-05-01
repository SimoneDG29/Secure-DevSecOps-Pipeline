from app import app

def test_api_endpoint():
    client = app.test_client()
    response = client.get("/api")
    assert response.status_code == 200
    assert response.get_json() == {"data": "Hello from api-service"}

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}