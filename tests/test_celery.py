import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.worker import celery
from app.worker.tasks import add_with_retry
from celery.result import AsyncResult


def test_add():
    task = add_with_retry.delay(2, 2)
    result = AsyncResult(task.id, app=celery)
    result.get(timeout=10)
    assert result.result == 4


if __name__ == '__main__':
    test_add()
