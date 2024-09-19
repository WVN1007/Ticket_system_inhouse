"""setup database data for tests"""

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL, create_engine
from app.database import app_config, get_db, Base
from app.main import app

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
TestingSessionLocal = sessionmaker(autoflush=False, bind=TestEngine)

@pytest.fixture()
def session():
    """manage the test's database data for each session"""
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
    '''return a TestClient instant with all our fixtures'''
    def override_get_db():
        try:
            # we run our sessions() method before each sessions
            yield session # yield the session artefacts
        finally:
            session.close()
    
    # override our get_db dependencies
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)