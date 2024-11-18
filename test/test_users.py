"""Tests for CRUD of Users and Devs"""

from .database_fixture import session, client, test_user
from app import schemas, db_model, utils
from app.database import app_config
import uuid
import jwt


def test_login_user(test_user, client):
    config = app_config
    res = client.post(
        "/api/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        config["SECRET_KEY"],
        algorithms=[config["ALGORITHMS"]],
    )
    id = payload.get("uid")
    assert uuid.UUID(id) == uuid.UUID(test_user["uid"])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


def test_create_users(client):
    res = client.post(
        "/api/users",
        json={
            "username": "User Tester",
            "role": "USER",
            "email": "tester@example.com",
            "password": "VerySecure",
        },
    )
    res_dict = {**res.json()}
    # print("::response returned from api: ", res_dict)
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "tester@example.com"


def test_get_users(session, client, test_user):
    data = [
        {
            "username": "User1 no Tester",
            "role": "USER",
            "email": "tester1@example.com",
            "password": utils.hash_pwd("VerySecure"),
            "tickets": [],
        },
        {
            "username": "User2 no Tester",
            "role": "USER",
            "email": "tester2@example.com",
            "password": utils.hash_pwd("VerySecure"),
            "tickets": [],
        },
    ]

    def make_User_model(user_data):
        return db_model.User(**user_data)

    mapped_user = map(make_User_model, data)
    user_list = list(mapped_user)
    session.add_all(user_list)
    session.commit()

    res = client.get("/api/users")
    users_detail = res.json()
    assert isinstance(users_detail, list)
    assert len(users_detail) == 3


def test_get_single_users(client, test_user):
    res = client.get(f"/api/users/{test_user['uid']}")
    assert res.status_code == 200
    user = res.json()
    assert user["uid"] == test_user["uid"]
    assert user["email"] == test_user["email"]


def test_update_single_users(client, test_user):
    id = str(test_user["uid"])
    ud = {
        "username": test_user["username"],
        "role": "ADMIN",
        "email": test_user["email"],
    }
    res = client.put(f"/api/users/{id}", json=ud)
    assert res.status_code == 200
    assert res.json()["uid"] == id
    assert res.json()["role"] == "ADMIN"


def test_delete_single_user(client, test_user):
    id = str(test_user["uid"])
    res = client.delete(f"/api/users/{id}")
    assert res.status_code == 204
    res = client.get(f"/api/users/{id}")
    assert res.status_code == 404
    fake_id = uuid.uuid4().hex
    res = client.delete(f"/api/users/{fake_id}")
    assert res.status_code == 404
