from app.worker import celery
from app.logging import logger
from celery.exceptions import MaxRetriesExceededError


@celery.task
async def add(x, y):
    result = x + y
    task = Task(task_id=add.request.id, status="completed", result=result)
    await task.insert()
    return result