import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_get_result():
    task_id = '577b1597-cb4a-423f-9907-494e791d45b4'
    response = client.get(f'/task/{task_id}')
    assert response.status_code == 200

if __name__ == '__main__':
    test_get_result()
