def test_register_success(client):
    res = client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "secret123"},
    )
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_username(client):
    client.post(
        "/api/auth/register",
        json={"username": "dup", "password": "secret123"},
    )
    res = client.post(
        "/api/auth/register",
        json={"username": "dup", "password": "secret123"},
    )
    assert res.status_code == 400


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"username": "loginuser", "password": "secret123"},
    )
    res = client.post(
        "/api/auth/login",
        json={"username": "loginuser", "password": "secret123"},
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_invalid_credentials(client):
    res = client.post(
        "/api/auth/login",
        json={"username": "noone", "password": "wrong"},
    )
    assert res.status_code == 401
