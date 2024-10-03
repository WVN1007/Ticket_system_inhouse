from fastapi import testclient
from app.main import app
from app.database import url_object
from app.settings import app_config
import psycopg
from sqlalchemy import create_engine

client = testclient.TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg":"Hello World"}

def test_database_connection():
    '''
    Assert that the following conn raise no exception
    '''
    try:
        DB_USERNAME = app_config["DB_USERNAME"]
        DB_PASS = app_config["DB_PASS"]
        DB_HOST = app_config["DB_HOST"]
        DB_NAME = app_config["DB_NAME"]
        DB_PORT = app_config["DB_PORT"]
        # print(f'{url_object}')
        psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASS,
            port=DB_PORT,
        )
        create_engine(url_object,echo=True)
    except Exception as e:
        assert False, f"test_database_connection raise exception {e}"

