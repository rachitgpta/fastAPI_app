from fastapi.testclient import TestClient
from app import schemas
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200


def test_create_user():
    res = client.post("/users/", json={"email": "hello3@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello3@gmail.com"
