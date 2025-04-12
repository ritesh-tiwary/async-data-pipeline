from app.worker import celery
from app.logging import Logger
from celery.exceptions import MaxRetriesExceededError


logger = Logger(__name__)

@celery.task(name='app.worker.tasks.add', bind=True, max_retries=3)
def add_with_retry(self, x, y):
    """
    Add two numbers together with retry logic and log the result.
    """
    try:
        result = x + y
        # task = Task(task_id=add_with_retry.request.id, status="completed", result=result)
        # await task.insert()
        return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)  # Retry after 5 seconds
