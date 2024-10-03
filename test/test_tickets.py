"""Ticket routers api tests"""

from app import schemas
from .database_fixture import (
    session,
    test_user,
    test_dev,
    test_tickets,
    authed_client,
    client,
    token_fixture,
)


def test_create_ticket(test_user, test_dev, authed_client):
    """
    A fixture commit tests ticket
    created by authed user
    and assigned to test_dev
    """
    tickets_data = {
        "typ": "INC",
        "status": "1",
        "state": "1",
        "severity": "1",
        "description": "a test tickets created by fixtures",
        "assign_to_id" : test_dev["uid"]
    }
    res = authed_client.post("/api/tickets/inc", json=tickets_data)
    # print("debug from test:", res.json())
    assert res.status_code == 201
    res_data = res.json()
    assert res_data["owner_id"] == test_user["uid"]
    assert res_data["assign_to_id"] == test_dev["uid"]
