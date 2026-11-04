from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_reports_foundation():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["phase"] == "foundation"

def test_dashboard_is_empty_without_invented_assets():
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["applications"] == 0
    assert data["servers"] == 0
    assert data["recent_alerts"] == []
