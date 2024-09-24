"""Tests for CRUD of Users and Devs"""
from .database_fixture import session, client
from app import schemas


def test_create_users(client):
    res = client.post(
        "/api/users",
        json={
            "username": "User Tester",
            "role": "USER",
            "email": "tester@example.com",
            "password": "VerySecure",
            "tickets": []
        },
    )
    res_dict = {**res.json()}
    print("::response returned from api: ",res_dict)
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "tester@example.com"
