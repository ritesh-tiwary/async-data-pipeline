from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_result():
    response = client.get("/result/", params={"task_id": "e89911a5-8830-42c9-857f-75b49ac19c13"})
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "Pending"
