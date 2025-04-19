from os import path
from app.worker import celery
from app.logging import Logger
from celery.exceptions import MaxRetriesExceededError


logger = Logger(__name__)

@celery.task(name='app.worker.tasks.save', bind=True, max_retries=3)
def save_data(self, filename: str, content: bytes):
    """
    Parse data
    """
    try:
        upload_path = path.join('uploads', filename)
        with open(upload_path, 'wb') as f:
            f.write(content)
        logger.info(f"File {upload_path} ({len(content)} bytes) saved successfully.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)

@celery.task(name='app.worker.tasks.parse', bind=True, max_retries=3)
def parse_data(self, bytes_obj: bytes):
    """
    Parse data
    """
    try:
        logger.info(len(bytes_obj))
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)

@celery.task(name='app.worker.tasks.load', bind=True, max_retries=3)
def load_data(self):
    """
    Load data
    """
    try:
        logger.info('Data loader started')
        # task = Task(task_id=add_with_retry.request.id, status="completed", result=result)
        # await task.insert()
        logger.info('Data loader finished')
    except MaxRetriesExceededError:
        logger.error(f"Max retries exceeded for file {filename}.")
        raise
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)  # Retry after 5 seconds

@celery.task(name='app.worker.tasks.add', bind=True, max_retries=3)
def add_with_retry(self, x, y):
    """
    Add two numbers together with retry logic and log the result.
    """
    try:
        result = x + y
        return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)  # Retry after 5 seconds
