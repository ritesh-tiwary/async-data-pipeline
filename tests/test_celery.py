from celery.result import AsyncResult
from app.tasks.task import save_to_db

def test_celery_save_to_db():
    task = save_to_db.delay(2, 3)
    result = AsyncResult(task.id)
    result.get(timeout=10)
    assert result.result == 5