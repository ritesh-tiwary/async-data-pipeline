from os import path
from app.worker import celery
from app.logging import Logger
from app.core.parser import get_parser
from app.api.v1.models.storage_model import FileTaskPayload


logger = Logger(__name__)

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

@celery.task(name='app.worker.tasks.parse', bind=True, max_retries=3)
def parse_data(self, payload_dict: dict):
    """
    Parse data
    """
    try:
        payload = FileTaskPayload(**payload_dict)
        with open(payload.filepath, 'rb') as f:
            content= f.read()
        logger.info(f"Processing file {payload.filename} at {payload.filepath}")
        parser = get_parser(payload.filename)
        parsed_file = parser.parse(payload.filepath)
        if bool(parsed_file):
            return parsed_file
        else:
            return "Parsing failed"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)

@celery.task(name='app.worker.tasks.load', bind=True, max_retries=3)
def load_data(self, filepath: str, payload_dict: dict):
    """
    Load data
    """
    try:
        payload = FileTaskPayload(**payload_dict)
        mapping_name = payload.info["mapping"]
        mapping_path = path.join("app/mapping", payload.info["mapping"])

        parser = get_parser(payload.filename)
        row_count = parser.load(filepath, mapping_name, mapping_path)
        if bool(row_count):
            return f"{row_count} rows loaded successfully"
        else:
            return "Loading failed"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise self.retry(exc=e, countdown=5)  # Retry after 5 seconds
