import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal, get_db
import os

# Use a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_addresses.db"

@pytest.fixture(scope="module")
def db_fixture():
    # Setup test DB
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Cleanup
        if os.path.exists("./test_addresses.db"):
            try:
                os.remove("./test_addresses.db")
            except PermissionError:
                pass

client = TestClient(app)

def test_create_address():
    response = client.post(
        "/addresses/",
        json={"name": "Berlin", "latitude": 52.5200, "longitude": 13.4050}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Berlin"
    assert "id" in data

def test_read_addresses():
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_distance():
    # Create Berlin
    client.post(
        "/addresses/",
        json={"name": "Berlin", "latitude": 52.5200, "longitude": 13.4050}
    )
    # Create Potsdam (approx 27km from Berlin center)
    client.post(
        "/addresses/",
        json={"name": "Potsdam", "latitude": 52.3906, "longitude": 13.0645}
    )
    
    # Search within 30km of Berlin
    response = client.get("/search/?lat=52.5200&lon=13.4050&dist=30")
    assert response.status_code == 200
    data = response.json()
    names = [addr["name"] for addr in data]
    assert "Berlin" in names
    assert "Potsdam" in names

    # Search within 10km of Berlin (should exclude Potsdam)
    response = client.get("/search/?lat=52.5200&lon=13.4050&dist=10")
    assert response.status_code == 200
    data = response.json()
    names = [addr["name"] for addr in data]
    assert "Berlin" in names
    assert "Potsdam" not in names

def test_update_address():
    # Create address
    res = client.post(
        "/addresses/",
        json={"name": "Old Name", "latitude": 0.0, "longitude": 0.0}
    )
    addr_id = res.json()["id"]
    
    # Update name
    response = client.patch(f"/addresses/{addr_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_delete_address():
    # Create address
    res = client.post(
        "/addresses/",
        json={"name": "To Delete", "latitude": 0.0, "longitude": 0.0}
    )
    addr_id = res.json()["id"]
    
    # Delete
    response = client.delete(f"/addresses/{addr_id}")
    assert response.status_code == 204
    
    # Verify 404
    response = client.get(f"/addresses/{addr_id}")
    assert response.status_code == 404
