"""setup database data for tests"""

from datetime import timedelta
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL, create_engine, select
from app import db_model
from app.database import app_config, get_db, Base
from app.main import app
from app.oauth_utils import create_access_token

# create a database engine
DB_ENGINE = app_config["DB_ENGINE"]
DB_USERNAME = app_config["DB_USERNAME"]
DB_PASS = app_config["DB_PASS"]
DB_HOST = app_config["DB_HOST"]
DB_NAME = app_config["DB_NAME"]
DB_PORT = app_config["DB_PORT"]

testdb_name = f"{DB_NAME}_test"
port = int(DB_PORT)

url_object = URL.create(
    f"postgresql+{DB_ENGINE}",
    username=DB_USERNAME,
    password=DB_PASS,
    host=DB_HOST,
    database=testdb_name,
    port=port,
)

TestEngine = create_engine(url_object)
TestingSessionLocal = sessionmaker(
    autoflush=False, bind=TestEngine, autocommit=False
)


@pytest.fixture()
def session():
    """manage the test's database data for each tests session"""
    # Drop all previous tests database data
    Base.metadata.drop_all(bind=TestEngine)
    # Recreate the tables
    Base.metadata.create_all(bind=TestEngine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    """return a TestClient instant with all our fixtures"""

    def override_get_db():
        try:
            # we run our sessions() method before each sessions
            yield session  # yield the session artefacts
        finally:
            session.close()

    # override our get_db dependencies
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    """using the test client, create a test_user"""
    user = {
        "username": "User1 no fixture",
        "role": "USER",
        "email": "Fixturetester1@example.com",
        "password": "VeryFixSecure",
        "tickets": [],
    }
    res = client.post("/api/users", json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user


@pytest.fixture()
def test_dev(client):
    """using the test client, create a test_staff"""
    staff = {
        "username": "Sta1 no fixture",
        "role": "STAFF",
        "email": "FixtureStaff1@example.com",
        "password": "VeryStaffFixSecure",
        "assigned_tickets": [],
    }
    res = client.post("/api/devs", json=staff)
    assert res.status_code == 201
    new_staff = res.json()
    new_staff["password"] = staff["password"]
    return new_staff


@pytest.fixture()
def token_fixture(test_user):
    """create a token for test_user"""
    env_token_exp = app_config["ACCESS_TOKEN_EXPIRE_MINUTES"]
    delta = timedelta(int(env_token_exp))
    token = create_access_token(
        data={"sub": test_user["username"], "uid": test_user["uid"]},
        expires_delta=delta,
    )
    return token


@pytest.fixture()
def authed_client(client, token_fixture):
    """use the created token, authorized the user"""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_fixture}",
    }

    return client


@pytest.fixture()
def test_tickets(test_user, test_dev, session):
    """
    A fixture commit tests ticket
    created by authed user
    and assigned to test_dev
    """
    in_db_user = session.execute(
        select(db_model.User).filter_by(uid=test_user["uid"])
    ).scalar_one_or_none()
    in_db_dev = session.execute(
        select(db_model.Dev).filter_by(uid=test_dev["uid"])
    ).scalar_one_or_none()
    tickets_data = {
        "typ": "INC",
        "status": "1",
        "state": "1",
        "severity": "1",
        "owner_id": test_user["uid"],
        "owner": in_db_user,
        "assign_to_id": test_dev["uid"],
        "assign_to": in_db_dev,
        "description": "a test tickets created by fixtures",
    }
    tickets_data_2 = {
            "typ": "INC",
            "status": "0",
            "state": "1",
            "severity": "1",
            "owner_id": test_user["uid"],
            "owner": in_db_user,
            "assign_to_id": test_dev["uid"],
            "assign_to": in_db_dev,
            "description": "another test tickets created by fixtures",
        }
    tickets = [db_model.Ticket(**tickets_data),db_model.Ticket(**tickets_data_2)]
    session.add_all(tickets)
    session.commit()

    db_tickets = session.execute(select(db_model.Ticket)).all()
    
    return db_tickets
