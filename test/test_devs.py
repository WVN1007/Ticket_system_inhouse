"""Tests for CRUD of Users and Devs"""

from .database_fixture import session, client,test_dev
from app import schemas, db_model, utils


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
    res_dict = {**res.json()}
    print("::response returned from api: ", res_dict)
    new_staff = schemas.DevOut(**res.json())
    assert res.status_code == 201
    assert new_staff.email == "Stafmember@example.com"


def test_get_staffs(session, client, test_dev):
    data = [
        {
            "username": "Staff1 no Test",
            "role": "STAFF",
            "email": "Staffmem1@example.com",
            "password": utils.hash_pwd('VeryStaffSecure'),
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
    assert staff['uid'] == test_dev['uid']
    assert staff['email'] == test_dev['email']
