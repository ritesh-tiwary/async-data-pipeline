from os import path
from app.worker import celery
from app.logging import Logger
from app.core.parser import get_parser
from celery.exceptions import MaxRetriesExceededError
from app.api.v1.models.storage_model import FileTaskPayload


logger = Logger(__name__)

@celery.task(name='app.worker.tasks.save', bind=True, max_retries=3)
def save_data(self, payload_dict: dict):
    """
    Parse data
    """
    try:
        payload = FileTaskPayload(**payload_dict)
        with open(payload.filepath, 'rb') as f:
            content= f.read()
        logger.info(f"Processing file {payload.filename} ({len(content)} bytes) at {payload.filepath}")
        return "Proccessed successfully"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)

@celery.task(name='app.worker.tasks.parse', bind=True, max_retries=3)
def parse_data(self, payload_dict: dict):
    """
    Parse data
    """
    try:
        payload = FileTaskPayload(**payload_dict)
        with open(payload.filepath, 'rb') as f:
            content= f.read()
        logger.info(f"Processing file {payload.filename} ({len(content)} bytes) at {payload.filepath}")
        
        parser = get_parser(payload.filename)
        if parser.parse(payload.filename, content):
            return "Parsed successfully"
        else:
            return "Parsing failed"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)

@celery.task(name='app.worker.tasks.load', bind=True, max_retries=3)
def load_data(self, payload_dict: dict):
    """
    Load data
    """
    try:
        payload = FileTaskPayload(**payload_dict)
        mapping_name = path.basename(payload.info["mapping"])
        mapping_path = payload.info["mapping"]

        with open(mapping_path, 'rb') as f:
            mapping= f.read()
        logger.info(f"Mapping file {mapping_name} ({len(mapping)} bytes) at {mapping_path}")

        with open(payload.filepath, 'rb') as f:
            content= f.read()
        logger.info(f"Loading file {payload.filename} ({len(content)} bytes) at {payload.filepath}")

        parser = get_parser(payload.filename)
        if parser.load(payload.filename, content, mapping_name, mapping):
            return "Loaded successfully"
        else:
            return "Loading failed"
        # task = Task(task_id=add_with_retry.request.id, status="completed", result=result)
        # await task.insert()
    except MaxRetriesExceededError:
        logger.error(f"Max retries exceeded for file {payload.filename}.")
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
