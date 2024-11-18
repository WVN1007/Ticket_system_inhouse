"""Tests for CRUD of Users and Devs"""

from .database_fixture import session, client, test_dev
from app import schemas, db_model, utils
from app.database import app_config
import uuid
import jwt


def test_login_dev(test_dev, client):
    config = app_config
    res = client.post(
        "/api/devs/login",
        data={
            "username": test_dev["username"],
            "password": test_dev["password"],
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        config["SECRET_KEY"],
        algorithms=[config["ALGORITHMS"]],
    )
    id = payload.get("uid")
    assert uuid.UUID(id) == uuid.UUID(test_dev["uid"])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


def test_create_devs(client):
    res = client.post(
        "/api/devs",
        json={
            "username": "Dev Tester",
            "role": "STAFF",
            "email": "Stafmember@example.com",
            "password": "VeryStaffSecure",
            "assigned_tickets": [],
        },
    )
    # res_dict = {**res.json()}
    # print("::response returned from api: ", res_dict)
    new_staff = schemas.DevOut(**res.json())
    assert res.status_code == 201
    assert new_staff.email == "Stafmember@example.com"


def test_get_staffs(session, client, test_dev):
    data = [
        {
            "username": "Staff1 no Test",
            "role": "STAFF",
            "email": "Staffmem1@example.com",
            "password": utils.hash_pwd("VeryStaffSecure"),
            "assigned_tickets": [],
        },
        {
            "username": "Staff2 no Test",
            "role": "STAFF",
            "email": "Staffmem2@example.com",
            "password": utils.hash_pwd("VeryStaffSecure"),
            "assigned_tickets": [],
        },
    ]

    def make_staff_model(staff_data):
        return db_model.Dev(**staff_data)

    mapped_staff = map(make_staff_model, data)
    staff_list = list(mapped_staff)
    session.add_all(staff_list)
    session.commit()

    res = client.get("/api/devs")
    users_detail = res.json()
    assert isinstance(users_detail, list)
    assert len(users_detail) == 3


def test_get_single_staffs(client, test_dev):
    res = client.get(f"/api/devs/{test_dev['uid']}")
    assert res.status_code == 200
    staff = res.json()
    assert staff["uid"] == test_dev["uid"]
    assert staff["email"] == test_dev["email"]


def test_update_single_dev(client, test_dev):
    id = str(test_dev["uid"])
    # print("staff_id", id)
    update = {
        "username": test_dev["username"],
        "role": "ADMIN",
        "email": test_dev["email"],
    }
    res = client.put(f"/api/devs/{id}", json=update)
    assert res.status_code == 200
    assert res.json()["role"] == "ADMIN"


def test_delete_single_dev(client, test_dev):
    id = str(test_dev["uid"])
    res = client.delete(f"/api/devs/{id}")
    assert res.status_code == 204
    res = client.get(f"/api/devs/{id}")
    assert res.status_code == 404
    fake_id = uuid.uuid4().hex
    res = client.delete(f"/api/devs/{fake_id}")
    assert res.status_code == 404
