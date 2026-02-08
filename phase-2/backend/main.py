"""Basic test to verify the backend application can start"""
# app/main.py
from fastapi import FastAPI

app = FastAPI()

# ... baki imports



def test_read_main():
    """Test the main endpoint"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome to Todo Backend API" in data["message"]


def test_health_endpoint():
    """Test the health endpoint"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "Todo Backend API"


def test_api_docs_available():
    """Test that API documentation is available"""
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_available():
    """Test that ReDoc documentation is available"""
    client = TestClient(app)
    response = client.get("/redoc")
    assert response.status_code == 200