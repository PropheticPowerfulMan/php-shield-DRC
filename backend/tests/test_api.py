from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Base, Role, User
from app.security import hash_password
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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

@pytest.fixture
def auth_client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestingSession.begin() as db:
        role = Role(name="Security Auditor")
        db.add(role)
        db.add(User(email="auditor@example.cd", password_hash=hash_password("a-long-test-password-42"), roles=[role]))

    def override_db():
        with TestingSession() as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()

def test_login_sets_http_only_session_and_me_returns_identity(auth_client):
    response = auth_client.post("/api/v1/auth/login", json={"email": "Auditor@Example.CD", "password": "a-long-test-password-42"})
    assert response.status_code == 200
    assert response.json()["roles"] == ["Security Auditor"]
    assert "php_shield_session" in response.cookies
    assert "httponly" in response.headers["set-cookie"].lower()
    assert auth_client.get("/api/v1/auth/me").json()["email"] == "auditor@example.cd"

def test_login_rejects_bad_password_and_logout_clears_session(auth_client):
    bad = auth_client.post("/api/v1/auth/login", json={"email": "auditor@example.cd", "password": "wrong"})
    assert bad.status_code == 401
    assert auth_client.get("/api/v1/auth/me").status_code == 401
    auth_client.post("/api/v1/auth/login", json={"email": "auditor@example.cd", "password": "a-long-test-password-42"})
    assert auth_client.post("/api/v1/auth/logout").status_code == 204
    assert auth_client.get("/api/v1/auth/me").status_code == 401
