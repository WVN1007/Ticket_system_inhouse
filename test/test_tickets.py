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
        "assign_to_id": test_dev["uid"],
    }
    res = authed_client.post("/api/tickets/inc", json=tickets_data)
    # print("debug from test:", res.json())
    assert res.status_code == 201
    res_data = res.json()
    assert res_data["owner_id"] == test_user["uid"]
    assert res_data["assign_to_id"] == test_dev["uid"]


def test_get_tickets_with_login(
    test_user, test_dev, test_tickets, authed_client
):
    res = authed_client.get("/api/tickets")

    def validate(ticket):
        return schemas.TicketOut(**ticket)

    tickets_map = map(validate, res.json())
    ticket_list = list(tickets_map)
    # print("lists of tests ticket", ticket_list)
    assert len(ticket_list) == len(test_tickets)
    assert res.status_code == 200
    print("Ticket_lists returns:", res.json())


def test_get_tickets_not_login(test_user, test_dev, test_tickets, client):
    res = client.get("/api/tickets")
    assert res.status_code == 200


def test_get_single_ticket_with_login(
    test_user, test_dev, test_tickets, authed_client
):
    ticket_one_db = test_tickets[1]
    id = str(ticket_one_db.uid)
    print(id)
    res = authed_client.get(f"/api/tickets/{id}")
    assert res.status_code == 200
    ticket = res.json()
    print(ticket)



def test_get_single_ticket_not_login(test_user, test_dev, test_tickets, client):
    ticket_one_db = test_tickets[0]
    id = str(ticket_one_db.uid)
    res = client.get(f"/api/tickets/{id}")
    assert res.status_code == 200
