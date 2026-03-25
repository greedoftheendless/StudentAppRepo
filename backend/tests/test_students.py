def test_add_student_success(client, auth_token):
    res = client.post(
        "/api/students/",
        json={"name": "Alice", "age": 20, "email": "alice@example.com"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_add_student_duplicate_email(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post(
        "/api/students/",
        json={"name": "Bob", "age": 22, "email": "bob@example.com"},
        headers=headers,
    )
    res = client.post(
        "/api/students/",
        json={"name": "Bob2", "age": 23, "email": "bob@example.com"},
        headers=headers,
    )
    assert res.status_code == 400


def test_add_student_unauthorized(client):
    res = client.post(
        "/api/students/",
        json={"name": "Eve", "age": 19, "email": "eve@example.com"},
    )
    assert res.status_code == 401


def test_list_students(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post(
        "/api/students/",
        json={"name": "Carol", "age": 21, "email": "carol@example.com"},
        headers=headers,
    )
    res = client.get("/api/students/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 1


def test_list_students_unauthorized(client):
    res = client.get("/api/students/")
    assert res.status_code == 401
