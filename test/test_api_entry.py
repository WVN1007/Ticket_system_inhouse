from fastapi import testclient
from app.main import app

client = testclient.TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg":"Hello World"}
