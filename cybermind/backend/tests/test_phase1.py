import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.llm import MockProvider

client = TestClient(app)

def test_health_checks():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CyberMIND"
    
    api_resp = client.get("/api/health")
    assert api_resp.status_code == 200
    assert api_resp.json()["status"] == "healthy"

def test_security_headers():
    response = client.get("/health")
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"

def test_password_hashing():
    pw = "CyberSecP@ssw0rd2026!"
    hashed = get_password_hash(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("wrongpass", hashed) is False

def test_auth_workflow():
    import uuid
    uid = uuid.uuid4().hex[:8]
    unique_user = f"secops_{uid}"
    unique_email = f"secops_{uid}@cybermind.local"
    pw = "SuperSecurePassword123!"

    # 1. Register
    reg_resp = client.post("/api/auth/register", json={
        "username": unique_user,
        "email": unique_email,
        "password": pw,
        "full_name": "SecOps Administrator",
        "role": "ADMIN"
    })
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["username"] == unique_user
    assert reg_data["user"]["role"] == "ADMIN"
    
    # Duplicate registration check
    dup_resp = client.post("/api/auth/register", json={
        "username": unique_user,
        "email": unique_email,
        "password": pw,
        "role": "ADMIN"
    })
    assert dup_resp.status_code == 400

    # 2. Login
    login_resp = client.post("/api/auth/login", json={
        "username_or_email": unique_user,
        "password": pw
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    token = login_data["access_token"]
    assert token is not None

    # Invalid login
    bad_login = client.post("/api/auth/login", json={
        "username_or_email": unique_user,
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401

    # 3. GET /me (Authorized)
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == unique_email

    # Unauthorized access check
    unauth_resp = client.get("/api/auth/me")
    assert unauth_resp.status_code == 401

    # 4. Logout
    logout_resp = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_resp.status_code == 200

@pytest.mark.asyncio
async def test_mock_llm_provider():
    provider = MockProvider()
    
    # Web Security
    web_res = await provider.generate("Explain SQL injection attack in web applications")
    assert web_res["domain"] == "Web Security"
    assert len(web_res["findings"]) > 0
    assert len(web_res["recommendations"]) > 0
    assert len(web_res["sources"]) > 0
    
    # API Security
    api_res = await provider.generate("What happens if API-01 becomes public?")
    assert api_res["domain"] == "API Security"
    assert "API-01" in api_res["findings"][0]["title"]
