"""Tests for CRUD of Users and Devs"""

from .database_fixture import session, client, test_user
from app import schemas, db_model
from requests import HTTPError


def test_create_users(client):
    res = client.post(
        "/api/users",
        json={
            "username": "User Tester",
            "role": "USER",
            "email": "tester@example.com",
            "password": "VerySecure",
            "tickets": [],
        },
    )
    res_dict = {**res.json()}
    print("::response returned from api: ", res_dict)
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "tester@example.com"


def test_get_users(session, client, test_user):
    data = [
        {
            "username": "User1 no Tester",
            "role": "USER",
            "email": "tester1@example.com",
            "password": "VerySecure",
            "tickets": [],
        },
        {
            "username": "User2 no Tester",
            "role": "USER",
            "email": "tester2@example.com",
            "password": "VerySecure",
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
    assert user['uid'] == test_user['uid']
    assert user['email'] == test_user['email']
